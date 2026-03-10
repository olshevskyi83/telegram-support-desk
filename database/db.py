import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE_PATH = os.getenv("DATABASE_PATH", "support_desk.db")


def init_db() -> None:
    db_file = Path(DATABASE_PATH)
    with sqlite3.connect(db_file) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id TEXT NOT NULL,
                username TEXT,
                message_text TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_ticket(telegram_user_id: str, username: str | None, message_text: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tickets (telegram_user_id, username, message_text, status)
            VALUES (?, ?, ?, 'open')
            """,
            (telegram_user_id, username, message_text),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_tickets() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, telegram_user_id, username, message_text, status, created_at
            FROM tickets
            ORDER BY id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_ticket(ticket_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, telegram_user_id, username, message_text, status, created_at
            FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()
        return dict(row) if row else None


def update_ticket_status(ticket_id: int, status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE tickets
            SET status = ?
            WHERE id = ?
            """,
            (status, ticket_id),
        )
        conn.commit()
        return cursor.rowcount > 0