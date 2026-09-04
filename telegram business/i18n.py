"""English / Polish strings and per-user language storage."""
from __future__ import annotations

import json
import os
from typing import Any

from config import BUSINESS_NAME

LANG_FILE = os.path.join("data", "languages.json")
SUPPORTED = ("en", "pl")
DEFAULT_LANG = "en"

CHOOSE_LANGUAGE = "Language / Język"

TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "funnel_welcome": (
            "*{business_name}*\n\n"
            "Hi. Pick what you need — it takes about a minute."
        ),
        "menu_welcome": (
            "*{business_name}*\n\n"
            "Hi. Pick what you need — it takes about a minute."
        ),
        "commands_hint": "Buttons below: Menu · New · Help",
        "nav_placeholder": "Tap a button or type a message",
        "menu_actions_prompt": "What do you need?",
        "btn_nav_menu": "Menu",
        "btn_nav_new": "New",
        "btn_nav_help": "Help",
        "funnel_ask_category": "What do you need help with?",
        "funnel_ask_task": (
            "*{category}*\n\n"
            "Describe the problem in a short message,\n"
            "or send a *photo* of it."
        ),
        "funnel_ask_contact": (
            "Thanks. Last step — what number should we call?\n\n"
            "Type it here, for example `+1 555 123 4567`."
        ),
        "funnel_thanks": "Thanks, {name}. We'll call you shortly.",
        "funnel_need_contact": "Please send a phone number, for example `+1 555 123 4567`.",
        "funnel_type_phone_hint": "Just type the number here in the chat.",
        "funnel_need_task": "Send a short description, or a photo of the job.",
        "funnel_photo_received": "Thanks for the photo — that helps a lot.",
        "funnel_menu_after": "Need anything else?",
        "funnel_cancel": "Stopped. Send /start when you want to begin again.",
        "start_fallback": "What do you need?",
        "btn_new_request": "New request",
        "btn_start_request": "Send a request",
        "btn_claim_bonus": "New request",
        "btn_type_phone": "Send number",
        "btn_reviews": "⭐ Reviews & cases",
        "btn_cat_repair": "🔧 Repair & home services",
        "btn_cat_cleaning": "🧹 Cleaning",
        "btn_cat_other": "📋 Other",
        "cat_repair": "Repair & home services",
        "cat_cleaning": "Cleaning",
        "cat_other": "Other",
        "btn_cat_plumbing": "Plumbing",
        "btn_cat_electrical": "Electrical",
        "btn_cat_handyman": "Handyman",
        "btn_cat_garden": "Garden",
        "cat_plumbing": "Plumbing",
        "cat_electrical": "Electrical",
        "cat_handyman": "Handyman",
        "cat_garden": "Garden",
        "btn_services": "Services",
        "btn_pricing": "Prices",
        "btn_book": "Book a visit",
        "btn_contact": "Contact",
        "btn_back": "Back",
        "btn_language": "Language",
        "help": (
            "/start — menu\n"
            "/new — new request\n"
            "/cancel — stop"
        ),
        "services": (
            "*Services*\n\n"
            "• Repair & home — plumbing, electrical, handyman\n"
            "• Cleaning — regular and deep cleans\n"
            "• Other — tell us what you need"
        ),
        "pricing": (
            "*Prices, starting from*\n\n"
            "• Cleaning — $40 / visit\n"
            "• Repair & home — from $35 / hour\n\n"
            "Final price depends on the job."
        ),
        "contact": (
            "*Contact*\n\n"
            "Phone: +1 (555) 123-4567\n"
            "Email: hello@brighthomeservices.example\n"
            "123 Main St, Springfield\n"
            "Mon–Sat, 8:00–18:00"
        ),
        "reviews": (
            "⭐ *Reviews & cases*\n\n"
            "🧹 *Cleaning — kitchen deep clean*\n"
            "“They left everything spotless. Booking again.” — Anna\n\n"
            "🔧 *Repair — leak under the sink*\n"
            "“Same-day fix, clear price, no mess left behind.” — Mark\n\n"
            "💡 *Home services — new lighting*\n"
            "“Neat install and explained everything.” — Julia\n\n"
            "Ready when you are — pick a category below."
        ),
        "booking_intro": (
            "*Book a visit*\n\n"
            "What's your full name?\n\n"
            "You can send /cancel at any time."
        ),
        "booking_bad_name": "Please enter your full name.",
        "booking_ask_phone": "Thanks, {name}. What number should we call?",
        "booking_bad_phone": "Please send a phone number, for example `+1 555 123 4567`.",
        "booking_done": "Thanks, {name}. We'll confirm a time at {phone}.",
        "booking_cancel": "Booking stopped. Send /start to open the menu.",
    },
    "pl": {
        "funnel_welcome": (
            "*{business_name}*\n\n"
            "Cześć. Wybierz, z czym potrzebujesz pomocy — zajmie to chwilę."
        ),
        "menu_welcome": (
            "*{business_name}*\n\n"
            "Cześć. Wybierz, z czym potrzebujesz pomocy — zajmie to chwilę."
        ),
        "commands_hint": "Przyciski poniżej: Menu · Nowe · Pomoc",
        "nav_placeholder": "Wybierz przycisk lub napisz wiadomość",
        "menu_actions_prompt": "Z czym potrzebujesz pomocy?",
        "btn_nav_menu": "Menu",
        "btn_nav_new": "Nowe",
        "btn_nav_help": "Pomoc",
        "funnel_ask_category": "Z czym potrzebujesz pomocy?",
        "funnel_ask_task": (
            "*{category}*\n\n"
            "Opisz problem krótką wiadomością\n"
            "albo wyślij *zdjęcie*."
        ),
        "funnel_ask_contact": (
            "Dzięki. Ostatni krok — pod jaki numer zadzwonić?\n\n"
            "Wpisz go tutaj, na przykład `+48 600 000 000`."
        ),
        "funnel_thanks": "Dzięki, {name}. Wkrótce zadzwonimy.",
        "funnel_need_contact": "Wyślij numer telefonu, na przykład `+48 600 000 000`.",
        "funnel_type_phone_hint": "Wpisz numer tutaj, w czacie.",
        "funnel_need_task": "Napisz krótki opis albo wyślij zdjęcie.",
        "funnel_photo_received": "Dzięki za zdjęcie — bardzo pomaga.",
        "funnel_menu_after": "Coś jeszcze?",
        "funnel_cancel": "Przerwano. Wyślij /start, gdy będziesz gotowy.",
        "start_fallback": "Z czym potrzebujesz pomocy?",
        "btn_new_request": "Nowe zgłoszenie",
        "btn_start_request": "Wyślij zgłoszenie",
        "btn_claim_bonus": "Nowe zgłoszenie",
        "btn_type_phone": "Wyślę numer",
        "btn_reviews": "⭐ Opinie i przykłady",
        "btn_cat_repair": "🔧 Remont i usługi domowe",
        "btn_cat_cleaning": "🧹 Sprzątanie",
        "btn_cat_other": "📋 Inne",
        "cat_repair": "Remont i usługi domowe",
        "cat_cleaning": "Sprzątanie",
        "cat_other": "Inne",
        "btn_cat_plumbing": "Hydraulika",
        "btn_cat_electrical": "Elektryka",
        "btn_cat_handyman": "Naprawy",
        "btn_cat_garden": "Ogród",
        "cat_plumbing": "Hydraulika",
        "cat_electrical": "Elektryka",
        "cat_handyman": "Naprawy",
        "cat_garden": "Ogród",
        "btn_services": "Usługi",
        "btn_pricing": "Ceny",
        "btn_book": "Termin",
        "btn_contact": "Kontakt",
        "btn_back": "Wstecz",
        "btn_language": "Język",
        "help": (
            "/start — menu\n"
            "/new — nowe zgłoszenie\n"
            "/cancel — przerwij"
        ),
        "services": (
            "*Usługi*\n\n"
            "• Remont i dom — hydraulika, elektryka, naprawy\n"
            "• Sprzątanie — regularne i gruntowne\n"
            "• Inne — napisz, czego potrzebujesz"
        ),
        "pricing": (
            "*Ceny, od*\n\n"
            "• Sprzątanie — 40 USD / wizyta\n"
            "• Remont i dom — od 35 USD / godz.\n\n"
            "Ostateczna cena zależy od zakresu."
        ),
        "contact": (
            "*Kontakt*\n\n"
            "Telefon: +1 (555) 123-4567\n"
            "E-mail: hello@brighthomeservices.example\n"
            "123 Main St, Springfield\n"
            "Pon–sob, 8:00–18:00"
        ),
        "reviews": (
            "⭐ *Opinie i przykłady*\n\n"
            "🧹 *Sprzątanie — gruntowna kuchnia*\n"
            "„Wszystko lśni. Na pewno wrócę.” — Anna\n\n"
            "🔧 *Remont — przeciek pod zlewem*\n"
            "„Tego samego dnia, jasna cena, bez bałaganu.” — Marek\n\n"
            "💡 *Usługi domowe — nowe oświetlenie*\n"
            "„Czysty montaż i wszystko wyjaśnili.” — Julia\n\n"
            "Gdy będziesz gotowy — wybierz kategorię poniżej."
        ),
        "booking_intro": (
            "*Termin*\n\n"
            "Jak masz na imię i nazwisko?\n\n"
            "W każdej chwili możesz wysłać /cancel."
        ),
        "booking_bad_name": "Wpisz imię i nazwisko.",
        "booking_ask_phone": "Dzięki, {name}. Pod jaki numer zadzwonić?",
        "booking_bad_phone": "Wyślij numer telefonu, na przykład `+48 600 000 000`.",
        "booking_done": "Dzięki, {name}. Potwierdzimy termin pod numerem {phone}.",
        "booking_cancel": "Przerwano. Wyślij /start, aby wrócić do menu.",
    },
}


def _load() -> dict[str, str]:
    if not os.path.exists(LANG_FILE):
        return {}
    try:
        with open(LANG_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {str(k): v for k, v in data.items() if v in SUPPORTED}
    except (OSError, json.JSONDecodeError):
        return {}


def _save(mapping: dict[str, str]) -> None:
    directory = os.path.dirname(LANG_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def get_lang(user_id: int | None) -> str:
    if not user_id:
        return DEFAULT_LANG
    return _load().get(str(user_id), DEFAULT_LANG)


def has_lang(user_id: int | None) -> bool:
    """True if the user has already picked a language."""
    if not user_id:
        return False
    return str(user_id) in _load()


def set_lang(user_id: int, lang: str) -> str:
    lang = lang if lang in SUPPORTED else DEFAULT_LANG
    mapping = _load()
    mapping[str(user_id)] = lang
    _save(mapping)
    return lang


def t(lang: str, key: str, **kwargs: Any) -> str:
    """Return a translated string. Falls back to English if a key is missing."""
    lang = lang if lang in TEXTS else DEFAULT_LANG
    template = TEXTS[lang].get(key) or TEXTS[DEFAULT_LANG][key]
    if "business_name" not in kwargs:
        kwargs.setdefault("business_name", BUSINESS_NAME)
    return template.format(**kwargs)
