# Telegram Bot Portfolio (Wrocław)

Developer business-card bot that sells turnkey Telegram bots for business.
Built with [aiogram](https://docs.aiogram.dev/) 3, [FastAPI](https://fastapi.tiangolo.com/),
and [uvicorn](https://www.uvicorn.org/).

## What the bot does

- `/start` — language picker (EN / PL / RU / UK), then a welcome + inline menu
- **Order a bot** — funnel: niche → task → contact (@ or phone), saved to CSV
- **Examples & cases** — catalogs, multilingual, integrations
- **Pricing & timelines** — from 5–10 days, fixed price
- **Contact me** — your Telegram `@username`

**Locally:** long polling (`python main.py`).
**On Render:** FastAPI webhooks via uvicorn.

---

## Project structure

```
.
├── main.py                 # Entry — FastAPI + polling / webhook
├── bot.py                  # aiogram Bot and Dispatcher
├── config.py               # Env loading & logging
├── i18n.py                 # EN / PL / RU / UK strings
├── keyboards.py            # Inline menus
├── storage.py              # Inquiry CSV
├── handlers/
│   ├── commands.py         # /start, /help, language
│   ├── menu.py             # Cases / pricing / contact
│   └── funnel.py           # Order funnel FSM
├── data/
│   └── leads.csv           # Created at runtime
├── Procfile
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Setup

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` → `.env` and set:

```env
BOT_TOKEN=your_token_from_BotFather
CONTACT_USERNAME=your_telegram_username
BUSINESS_NAME=Telegram bots for business · Wrocław
ADMIN_CHAT_ID=   # optional: your numeric chat id for inquiry alerts
```

`CONTACT_USERNAME` is shown without `@` in `.env`; the bot displays `@{username}`.

---

## Run locally

```bash
python main.py
```

Open the bot in Telegram and send `/start`. Keep **one** process only — two instances cause `TelegramConflictError`.

---

## Deploy on Render

1. Set env vars: `BOT_TOKEN`, `CONTACT_USERNAME`, optionally `ADMIN_CHAT_ID`, `WEBHOOK_SECRET`.
2. `WEBHOOK_URL` can be left empty — Render’s `RENDER_EXTERNAL_URL` is used when present.
3. `Procfile` starts uvicorn; Telegram posts updates to `WEBHOOK_PATH` (default `/webhook`).

---

## Leads

Inquiries land in `data/leads.csv` (niche, task, contact, Telegram user).
If `ADMIN_CHAT_ID` is set, you also get a Telegram notification.
