from dotenv import load_dotenv
import os

load_dotenv()

# Telegram bot token
TOKEN = os.getenv("TOKEN")

# SQLite database filename
DATABASE_NAME = os.getenv("DATABASE_NAME", "users.db")

# Webhook configuration - set WEBHOOK_URL to your public HTTPS URL (e.g. https://example.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # public url, optional for local testing
# Path suffix for webhook (will be appended to WEBHOOK_URL). Keep a secret path if possible.
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/tg_webhook")

# HTTP server host/port for the webhook receiver / admin panel
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

# Simple admin token to protect admin panel (set in env)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change_me")

book_numbers = {
    "3345": "https://gdzbakulin.ru/8-klass/kratkie-soderzhaniya/kratkiy-pereskaz-8-klass-medinskiy-torkunov/",
    "3367": "https://gdzbakulin.ru/8-klass/kratkie-soderzhaniya/kratkiy-pereskaz-8-klass-pasechnik/",
    "3355": "https://gdzbakulin.ru/8-klass/kratkie-soderzhaniya/kratkiy-pereskaz-fizika-8-klass-uchebnik/",
    "3327": "https://gdzbakulin.ru/8-klass/kratkie-soderzhaniya/kratkiy-pereskaz-8-klass-bogolubov/",
}