# Telegram Support Desk

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-api-black)
![Telegram](https://img.shields.io/badge/telegram-bot-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Telegram Support Desk is a lightweight customer support system for small businesses.

It allows customers to send support messages through a Telegram bot, stores tickets in a SQLite database, and provides a small web-based admin panel for viewing and managing requests.

## Features

- Telegram bot for incoming support messages
- SQLite ticket storage
- Flask REST API
- simple admin web panel
- ticket status management
- Docker support

## Project Structure

```text
telegram-support-desk/
├── README.md
├── INSTALL.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── bot/
│   └── support_bot.py
├── api/
│   └── app.py
├── database/
│   ├── __init__.py
│   └── db.py
└── admin/
    └── panel.py
    Components
Telegram Bot

Receives messages from users and stores them as tickets.

API

Provides access to tickets and allows status updates.

Admin Panel

Displays tickets in a simple web interface.

Database

SQLite storage for support tickets.

Ticket Fields

Each ticket contains:

id

telegram user id

username

message text

status

created_at

Default Statuses

open

in_progress

closed

Quick Start

Install dependencies:

pip install -r requirements.txt

Run API:

python api/app.py

Run admin panel:

python admin/panel.py

Run bot:

python bot/support_bot.py
Environment Variables

See .env.example.

Example API Endpoints
Health
GET /health
List tickets
GET /tickets
Get ticket by id
GET /tickets/<id>
Update status
POST /tickets/<id>/status
Use Cases

support inbox for small businesses

Telegram-based help desk

customer communication logging

basic service request management
License

MIT


---

## `INSTALL.md`

```markdown
# Installation Guide

This guide installs Telegram Support Desk on a Linux machine.

## Requirements

- Python 3.10+
- pip
- Telegram bot token

## 1. Clone repository

```bash
git clone https://github.com/yourname/telegram-support-desk.git
cd telegram-support-desk
2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment

Create .env based on .env.example:

cp .env.example .env

Edit the file and set your Telegram bot token.

5. Start API
python api/app.py
6. Start admin panel

Open another terminal:

source .venv/bin/activate
python admin/panel.py
7. Start Telegram bot

Open another terminal:

source .venv/bin/activate
python bot/support_bot.py
Ports

API: 5001

Admin panel: 5002

Health check
curl http://127.0.0.1:5001/health
Docker
docker compose up --build

Guidelines

follow PEP8

keep code modular

prefer small functions

document API changes

test manually before submitting

Bug Reports

Please include:

Python version

operating system

exact error

logs

reproduction steps