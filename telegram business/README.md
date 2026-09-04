# Lead-Generation Telegram Bot

A production-ready Telegram bot template for a local service business, built
with [aiogram](https://docs.aiogram.dev/) 3, [FastAPI](https://fastapi.tiangolo.com/),
and [uvicorn](https://www.uvicorn.org/).

The bot acts as an interactive lead-generation assistant:

- 👋 Clean welcome message with an inline keyboard menu
- 🛠️ **Services** / 💰 **Pricing** / 📞 **Contact Us** — instant mock business info
- 📅 **Book Appointment** — a guided, multi-step conversation that collects the
  user's name and phone number
- 💾 Every booking is saved as a **lead** to a local CSV file and written to
  the application log (optionally forwarded to an admin chat in real time)

**Locally** the bot uses long polling (`python main.py`).
**On Render** it runs as a web service: FastAPI receives Telegram webhooks via uvicorn.

---

## Project Structure

```
.
├── main.py                 # Entry point — FastAPI app + polling / webhook
├── bot.py                  # aiogram Bot and Dispatcher
├── config.py               # Env var loading & logging setup
├── keyboards.py            # Inline keyboard builders / callback-data constants
├── mock_data.py            # Mock business copy (services, pricing, contact)
├── storage.py              # Lead persistence (CSV) + logging
├── handlers/
│   ├── start.py            # /start, /help, "Back to Menu"
│   ├── menu.py             # Services / Pricing / Contact Us handlers
│   └── booking.py          # Multi-step booking FSM
├── data/
│   └── leads.csv           # Created automatically at runtime
├── Procfile                # Render start command (web / uvicorn)
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 1. Prerequisites

- Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather):
  1. Open a chat with **@BotFather** on Telegram.
  2. Send `/newbot` and follow the prompts (choose a name and username).
  3. Copy the token it gives you — it looks like `123456789:AAExampleToken...`.

---

## 2. Setup

Clone/copy this project, then from the project root:

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

---

## 3. Configure the BOT_TOKEN

You have two options:

### Option A — `.env` file (recommended for local development)

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Then open `.env` and set your token:

```
BOT_TOKEN=123456789:AAExampleTokenReplaceThisWithYours
```

The bot loads `.env` automatically at startup (via `python-dotenv`).

### Option B — Real environment variable

**Windows (PowerShell):**

```powershell
$env:BOT_TOKEN = "123456789:AAExampleTokenReplaceThisWithYours"
```

**macOS / Linux (bash/zsh):**

```bash
export BOT_TOKEN="123456789:AAExampleTokenReplaceThisWithYours"
```

Other optional variables (see `.env.example`):

| Variable          | Default                  | Description                                              |
|-------------------|--------------------------|----------------------------------------------------------|
| `BUSINESS_NAME`   | `Bright Home Services`   | Name used in bot messages                                |
| `ADMIN_CHAT_ID`   | *(empty)*                | Chat ID that gets a message for every new lead           |
| `LEADS_FILE`      | `data/leads.csv`         | Path to the CSV file where leads are stored              |
| `LOG_LEVEL`       | `INFO`                   | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`)  |
| `WEBHOOK_URL`     | *(empty)*                | Public HTTPS base URL. Empty = local polling             |
| `WEBHOOK_PATH`    | `/webhook`               | Path Telegram POSTs updates to                           |
| `WEBHOOK_SECRET`  | *(empty)*                | Optional secret for `X-Telegram-Bot-Api-Secret-Token`    |
| `HOST` / `PORT`   | `0.0.0.0` / `8000`       | HTTP bind address (Render sets `PORT` automatically)     |

> **Tip:** To find your `ADMIN_CHAT_ID`, message [@userinfobot](https://t.me/userinfobot) on Telegram — it will reply with your numeric chat ID.

---

## 4. Run the bot locally

```bash
python main.py
```

You should see:

```
... | INFO | __main__ | Bot starting (polling mode)... Press Ctrl+C to stop.
```

Open Telegram, find your bot (by the username you chose in BotFather), and
send `/start`.

To test the FastAPI webhook server locally (without Telegram):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

`GET http://127.0.0.1:8000/` should return `{"status":"ok"}`.

---

## 5. Using the bot

- `/start` — shows the welcome message and main menu
- `/help` — quick usage tip
- `/cancel` — aborts an in-progress booking

**Main menu buttons:**

| Button              | Behavior                                                        |
|---------------------|-----------------------------------------------------------------|
| 🛠️ Services         | Shows a mock list of services                                   |
| 💰 Pricing          | Shows mock starting prices                                      |
| 📅 Book Appointment | Starts a 2-step conversation: asks for **name**, then **phone** |
| 📞 Contact Us       | Shows mock contact details                                      |

When a booking completes, the lead is:

1. Appended as a row to `data/leads.csv` (`timestamp, user_id, username, full_name, name, phone`)
2. Logged via the `leads` logger (visible in the console/log output)
3. Sent to `ADMIN_CHAT_ID` if configured

---

## 6. Deploy to Render

1. Push this repo to GitHub and create a **Web Service** on [Render](https://render.com)
   (not a Background Worker — the bot now listens on HTTP).
2. Render will read `Procfile`:

   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. Set environment variables in the Render dashboard:
   - `BOT_TOKEN` (required)
   - `WEBHOOK_SECRET` (recommended)
   - optional: `BUSINESS_NAME`, `ADMIN_CHAT_ID`, …
4. You typically do **not** need to set `WEBHOOK_URL` on Render: the bot falls
   back to `RENDER_EXTERNAL_URL` and registers `https://<your-app>.onrender.com/webhook`.

> `data/leads.csv` lives on an ephemeral disk. For production, attach a Render
> Disk or replace `storage.py` with a database.

---

## 7. Customizing

- **Business content:** edit `mock_data.py` (services, pricing, contact info, welcome text).
- **Menu layout:** edit `keyboards.py`.
- **Booking questions/validation:** edit `handlers/booking.py` (e.g. add an email step, change the phone regex).
- **Lead storage:** replace the CSV logic in `storage.py` with a database call, Google Sheets API, or CRM/webhook integration for production use.

---

## 8. Troubleshooting

- **`RuntimeError: BOT_TOKEN is not set`** — you haven't set the `BOT_TOKEN`
  environment variable or `.env` file. See step 3 above.
- **Bot doesn't respond** — make sure only one instance of the bot is running
  (Telegram allows either one poller **or** one webhook per token, not both).
- **`Conflict: terminated by other getUpdates request`** — another instance of
  the bot is still polling; stop it first, or switch fully to webhooks.
