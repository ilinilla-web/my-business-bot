"""Configuration loader for the developer portfolio bot."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = (TOKEN or "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set.\n"
        "Create a '.env' file (copy '.env.example') or set the BOT_TOKEN "
        "environment variable before starting the bot. See README.md for details."
    )

# Display name / brand line in messages.
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Telegram bots for business · Wrocław")

# Your Telegram username for "Contact me" (without @).
CONTACT_USERNAME = (os.getenv("CONTACT_USERNAME", "ilinilla") or "ilinilla").lstrip("@")

# Phone shown in Telegram / WhatsApp contact block.
CONTACT_PHONE = (os.getenv("CONTACT_PHONE", "+48510373906") or "+48510373906").strip()

# Digits only for wa.me links (defaults from CONTACT_PHONE).
_phone_digits = "".join(c for c in CONTACT_PHONE if c.isdigit())
CONTACT_WHATSAPP = (
    os.getenv("CONTACT_WHATSAPP", "").strip()
    or _phone_digits
    or "48510373906"
)
CONTACT_WHATSAPP_URL = f"https://wa.me/{CONTACT_WHATSAPP}"

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "").strip() or None
LEADS_FILE = os.getenv("LEADS_FILE", os.path.join("data", "leads.csv"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

WEBHOOK_URL = (
    os.getenv("WEBHOOK_URL", "").strip()
    or os.getenv("RENDER_EXTERNAL_URL", "").strip()
    or None
)
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip() or None


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        level=LOG_LEVEL,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
