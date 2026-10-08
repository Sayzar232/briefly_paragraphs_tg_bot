from dotenv import load_dotenv
import os

load_dotenv()

# Telegram bot token
TOKEN = os.getenv("TOKEN")

# PostgreSQL connection URL (DSN), e.g. postgresql://user:password@host:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# Webhook configuration - set WEBHOOK_URL to your public HTTPS URL (e.g. https://example.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # public url, optional for local testing
# Path suffix for webhook (will be appended to WEBHOOK_URL). Keep a secret path if possible.
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")

# HTTP server host/port for the webhook receiver / admin panel
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", 8000))

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change_me")  # secret path for webhook

# Simple admin token to protect admin panel (set in env)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change_me")