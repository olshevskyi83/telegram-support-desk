import os

from flask import Flask, redirect, render_template_string, request, url_for

from database.db import init_db, list_tickets, update_ticket_status

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Telegram Support Desk</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 24px;
            background: #f7f7f7;
            color: #222;
        }
        h1 {
            margin-bottom: 20px;
        }
        .ticket {
            background: white;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .meta {
            color: #666;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .status {
            font-weight: bold;
        }
        form {
            margin-top: 12px;
        }
        select, button {
            padding: 8px 10px;
            font-size: 14px;
        }
        .empty {
            color: #777;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Telegram Support Desk — Admin Panel</h1>

    {% if tickets %}
        {% for ticket in tickets %}
            <div class="ticket">
                <div><strong>Ticket #{{ ticket.id }}</strong></div>
                <div class="meta">
                    User ID: {{ ticket.telegram_user_id }} |
                    Username: {{ ticket.username or 'N/A' }} |
                    Created: {{ ticket.created_at }}
                </div>
                <div><strong>Message:</strong></div>
                <div>{{ ticket.message_text }}</div>
                <div class="meta">
                    Status: <span class="status">{{ ticket.status }}</span>
                </div>

                <form method="post" action="/update-status/{{ ticket.id }}">
                    <select name="status">
                        <option value="open" {% if ticket.status == 'open' %}selected{% endif %}>open</option>
                        <option value="in_progress" {% if ticket.status == 'in_progress' %}selected{% endif %}>in_progress</option>
                        <option value="closed" {% if ticket.status == 'closed' %}selected{% endif %}>closed</option>
                    </select>
                    <button type="submit">Update status</button>
                </form>
            </div>
        {% endfor %}
    {% else %}
        <p class="empty">No tickets yet.</p>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    tickets = list_tickets()
    return render_template_string(HTML_TEMPLATE, tickets=tickets)


@app.route("/update-status/<int:ticket_id>", methods=["POST"])
def update_status(ticket_id: int):
    status = request.form.get("status", "")
    if status in {"open", "in_progress", "closed"}:
        update_ticket_status(ticket_id, status)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    host = os.getenv("ADMIN_HOST", "127.0.0.1")
    port = int(os.getenv("ADMIN_PORT", "5002"))
    app.run(host=host, port=port, debug=True)