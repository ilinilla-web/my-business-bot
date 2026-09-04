"""Configuration loader for the bot.

All settings are read from environment variables. For local development you
can put them in a `.env` file (see `.env.example`) — it is loaded
automatically via python-dotenv.
"""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

# --- Required ---------------------------------------------------------------

TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = (TOKEN or "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set.\n"
        "Create a '.env' file (copy '.env.example') or set the BOT_TOKEN "
        "environment variable before starting the bot. See README.md for details."
    )

# --- Optional ----------------------------------------------------------------

# Name shown in bot copy (welcome message, confirmations, etc.).
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Bright Home Services")

# If set, this chat ID receives an instant notification for every new lead.
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "").strip() or None

# Where captured leads are persisted (CSV file, created automatically).
LEADS_FILE = os.getenv("LEADS_FILE", os.path.join("data", "leads.csv"))

# Log verbosity: DEBUG, INFO, WARNING, ERROR.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# HTTP server (used in webhook / Render mode). Render injects PORT automatically.
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Public HTTPS URL of this service, e.g. https://my-bot.onrender.com
# If empty, the bot runs in local polling mode instead of webhooks.
# On Render, RENDER_EXTERNAL_URL is used as a fallback when WEBHOOK_URL is unset.
WEBHOOK_URL = (
    os.getenv("WEBHOOK_URL", "").strip()
    or os.getenv("RENDER_EXTERNAL_URL", "").strip()
    or None
)
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip() or None


def configure_logging() -> None:
    """Configure application-wide logging. Call once at startup."""
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        level=LOG_LEVEL,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
