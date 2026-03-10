import os

from flask import Flask, jsonify, request

from database.db import get_ticket, init_db, list_tickets, update_ticket_status

app = Flask(__name__)

VALID_STATUSES = {"open", "in_progress", "closed"}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/tickets", methods=["GET"])
def tickets():
    return jsonify(list_tickets()), 200


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def ticket_by_id(ticket_id: int):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(ticket), 200


@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
def ticket_status(ticket_id: int):
    payload = request.get_json(silent=True) or {}
    status = payload.get("status")

    if status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    updated = update_ticket_status(ticket_id, status)
    if not updated:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({"message": "Status updated", "ticket_id": ticket_id, "status": status}), 200


if __name__ == "__main__":
    init_db()
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "5001"))
    app.run(host=host, port=port, debug=True)