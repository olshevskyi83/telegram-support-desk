import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from database.db import create_ticket, init_db

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Hello. Send me your support message and I will create a ticket."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Use this bot to send a support request. Just type your message."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    message_text = update.message.text or ""

    if not message_text.strip():
        await update.message.reply_text("Empty messages cannot be stored as tickets.")
        return

    ticket_id = create_ticket(
        telegram_user_id=str(user.id),
        username=user.username,
        message_text=message_text.strip(),
    )

    await update.message.reply_text(
        f"Your request has been received. Ticket ID: {ticket_id}"
    )


def check_api_health() -> None:
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = os.getenv("API_PORT", "5001")
    url = f"http://{api_host}:{api_port}/health"
    try:
        requests.get(url, timeout=3)
    except Exception:
        pass


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    init_db()
    check_api_health()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()