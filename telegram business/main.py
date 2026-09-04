"""Entry point for the developer portfolio Telegram bot.

Local (polling):
    python main.py

Render / production (webhooks via FastAPI):
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""
from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from bot import bot, dp
from config import HOST, PORT, WEBHOOK_PATH, WEBHOOK_SECRET, WEBHOOK_URL
from handlers.commands import setup_bot_commands

logger = logging.getLogger(__name__)


def _webhook_endpoint() -> str:
    """Full HTTPS URL Telegram should POST updates to."""
    base = (WEBHOOK_URL or "").rstrip("/")
    path = WEBHOOK_PATH if WEBHOOK_PATH.startswith("/") else f"/{WEBHOOK_PATH}"
    return f"{base}{path}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Register / drop the Telegram webhook around the FastAPI process lifetime."""
    if WEBHOOK_URL:
        url = _webhook_endpoint()
        await bot.set_webhook(
            url=url,
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True,
        )
        logger.info("Webhook registered: %s", url)
    await setup_bot_commands(bot)
    logger.info("Bot commands registered: /start /help /cancel")
    yield
    await bot.delete_webhook(drop_pending_updates=False)
    await bot.session.close()
    logger.info("Bot session closed.")


app = FastAPI(title="Telegram Bot Portfolio · Wrocław", lifespan=lifespan)


@app.get("/")
async def health() -> dict[str, str]:
    """Render (and load balancers) use this as a liveness check."""
    return {"status": "ok"}


@app.post(WEBHOOK_PATH)
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> JSONResponse:
    """Receive Telegram updates and feed them into aiogram."""
    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret token")

    payload = await request.json()
    update = Update.model_validate(payload, context={"bot": bot})
    await dp.feed_update(bot, update)
    return JSONResponse({"ok": True})


async def run_polling() -> None:
    """Local development: long-polling, no public URL required."""
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_bot_commands(bot)
    logger.info("Bot starting (polling mode)... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


def main() -> None:
    if WEBHOOK_URL:
        import uvicorn

        logger.info("Bot starting (webhook mode) on %s:%s ...", HOST, PORT)
        uvicorn.run("main:app", host=HOST, port=PORT, log_level="info")
        return

    asyncio.run(run_polling())


if __name__ == "__main__":
    main()
