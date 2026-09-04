"""i18n: English / Polish / Russian / Ukrainian."""
from __future__ import annotations

import json
import os
from typing import Any

from config import (
    BUSINESS_NAME,
    CONTACT_PHONE,
    CONTACT_USERNAME,
    CONTACT_WHATSAPP_URL,
)

LANG_FILE = os.path.join("data", "languages.json")
SUPPORTED = ("en", "pl", "ru", "uk")
DEFAULT_LANG = "en"

CHOOSE_LANGUAGE = "Language / Język / Язык / Мова"


TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "welcome": (
            "Hi! I build turnkey Telegram bots for business "
            "(automation, booking, catalogs, lead intake and photos).\n\n"
            "The bot you're in right now is a live example of my work.\n\n"
            "Based in *Wrocław*. How can I help?"
        ),
        "btn_order": "🚀 Order a bot / Discuss a project",
        "btn_cases": "💼 Examples & cases",
        "btn_pricing": "💰 Pricing & timelines",
        "btn_contact": "📞 Contact me",
        "btn_language": "🌐 Language",
        "btn_back": "⬅️ Back to menu",
        "cases": (
            "*Examples & cases*\n\n"
            "What I ship for businesses:\n\n"
            "• *Catalogs* — products/services with photos and prices\n"
            "• *Lead funnels* — niche → task → contact, saved to CRM/CSV\n"
            "• *Booking* — appointments and reminders\n"
            "• *Multilingual* — PL / EN / RU / UK and more\n"
            "• *Integrations* — Google Sheets, webhooks, payments, CRM\n"
            "• *Photo intake* — clients send photos of the job\n\n"
            "This bot itself is a portfolio piece you can walk through."
        ),
        "pricing": (
            "*Pricing & timelines*\n\n"
            "• Typical delivery: *from 5–10 days*\n"
            "• Fixed price per project (after a short brief)\n"
            "• Includes setup, basic training, and handoff\n\n"
            "Exact quote depends on features — tap *Order a bot* to discuss."
        ),
        "contact_me": (
            "*Contact me*\n\n"
            "Telegram: @{username}\n"
            "Phone / Telegram: {phone}\n"
            "WhatsApp: {whatsapp_url}\n"
            "Location: Wrocław, Poland\n\n"
            "Or tap *Order a bot* and leave your niche + task — I'll reply."
        ),
        "ask_niche": (
            "🚀 *Let's discuss your bot*\n\n"
            "What is your business niche?\n"
            "_(e.g. beauty salon, clinic, delivery, real estate)_"
        ),
        "ask_task": (
            "Got it — *{niche}*.\n\n"
            "What should the bot do?\n"
            "_(e.g. take bookings, show a catalog, collect leads with photos)_"
        ),
        "ask_contact": (
            "Almost done.\n\n"
            "How can I reach you? Send your *phone* or *@username*."
        ),
        "need_niche": "Please write a short niche (a few words).",
        "need_task": "Please describe the task in a short message.",
        "need_contact": "Send a phone number or @username.",
        "thanks": (
            "✅ Thanks! I received your request.\n\n"
            "Niche: {niche}\n"
            "Task: {task}\n"
            "Contact: {contact}\n\n"
            "I'll get back to you soon. You can also message @{username} directly."
        ),
        "cancelled": "Stopped. Send /start to open the menu again.",
        "help": (
            "/start — open the menu\n"
            "/cancel — stop an order in progress"
        ),
    },
    "pl": {
        "welcome": (
            "Cześć! Tworzę boty Telegram pod klucz dla biznesu "
            "(automatyzacja, rezerwacje, katalogi, zbieranie zgłoszeń i zdjęć).\n\n"
            "Bot, w którym jesteś, to żywy przykład mojej pracy.\n\n"
            "Działam we *Wrocławiu*. W czym mogę pomóc?"
        ),
        "btn_order": "🚀 Zamów bota / Omów projekt",
        "btn_cases": "💼 Przykłady i case'y",
        "btn_pricing": "💰 Ceny i terminy",
        "btn_contact": "📞 Napisz do mnie",
        "btn_language": "🌐 Język",
        "btn_back": "⬅️ Powrót do menu",
        "cases": (
            "*Przykłady i case'y*\n\n"
            "Co robię dla firm:\n\n"
            "• *Katalogi* — usługi/produkty ze zdjęciami i cenami\n"
            "• *Lejki leadów* — nisza → zadanie → kontakt\n"
            "• *Rezerwacje* — terminy i przypomnienia\n"
            "• *Wielojęzyczność* — PL / EN / RU / UK\n"
            "• *Integracje* — Google Sheets, webhooki, płatności, CRM\n"
            "• *Zdjęcia* — klienci wysyłają fotki zlecenia\n\n"
            "Ten bot sam w sobie jest portfolio — możesz go przejść."
        ),
        "pricing": (
            "*Ceny i terminy*\n\n"
            "• Typowy czas: *od 5–10 dni*\n"
            "• Stała cena projektu (po krótkim briefie)\n"
            "• W cenie: uruchomienie, krótkie wdrożenie, przekazanie\n\n"
            "Dokładna wycena zależy od funkcji — kliknij *Zamów bota*."
        ),
        "contact_me": (
            "*Kontakt*\n\n"
            "Telegram: @{username}\n"
            "Telefon / Telegram: {phone}\n"
            "WhatsApp: {whatsapp_url}\n"
            "Lokalizacja: Wrocław\n\n"
            "Albo kliknij *Zamów bota* i zostaw niszę + zadanie."
        ),
        "ask_niche": (
            "🚀 *Omówmy Twojego bota*\n\n"
            "Jaka jest nisza Twojego biznesu?\n"
            "_(np. salon beauty, klinika, dostawy, nieruchomości)_"
        ),
        "ask_task": (
            "Jasne — *{niche}*.\n\n"
            "Co ma robić bot?\n"
            "_(np. rezerwacje, katalog, zbieranie leadów ze zdjęciami)_"
        ),
        "ask_contact": (
            "Prawie gotowe.\n\n"
            "Jak mogę się odezwać? Wyślij *numer* albo *@username*."
        ),
        "need_niche": "Napisz krótko niszę (kilka słów).",
        "need_task": "Opisz zadanie krótką wiadomością.",
        "need_contact": "Wyślij numer telefonu albo @username.",
        "thanks": (
            "✅ Dzięki! Dostałem zgłoszenie.\n\n"
            "Nisza: {niche}\n"
            "Zadanie: {task}\n"
            "Kontakt: {contact}\n\n"
            "Odezwę się wkrótce. Możesz też napisać do @{username}."
        ),
        "cancelled": "Przerwano. Wyślij /start, aby wrócić do menu.",
        "help": (
            "/start — menu\n"
            "/cancel — przerwij zamówienie"
        ),
    },
    "ru": {
        "welcome": (
            "Привет! Я создаю Telegram-ботов под ключ для бизнеса "
            "(автоматизация, запись, каталоги, приём заявок и фото).\n\n"
            "Бот, в котором ты находишься — это живой пример моей работы.\n\n"
            "Работаю во *Вроцлаве*. Чем могу помочь?"
        ),
        "btn_order": "🚀 Заказать бота / Обсудить проект",
        "btn_cases": "💼 Примеры и кейсы",
        "btn_pricing": "💰 Стоимость и сроки",
        "btn_contact": "📞 Связаться со мной",
        "btn_language": "🌐 Язык",
        "btn_back": "⬅️ В меню",
        "cases": (
            "*Примеры и кейсы*\n\n"
            "Что умеют боты, которые я делаю:\n\n"
            "• *Каталоги* — услуги/товары с фото и ценами\n"
            "• *Воронки заявок* — ниша → задача → контакт\n"
            "• *Запись* — слоты и напоминания\n"
            "• *Мультиязычность* — PL / EN / RU / UK\n"
            "• *Интеграции* — Google Sheets, webhook, оплаты, CRM\n"
            "• *Приём фото* — клиент присылает фото задачи\n\n"
            "Этот бот — рабочее портфолио, можно пройти весь сценарий."
        ),
        "pricing": (
            "*Стоимость и сроки*\n\n"
            "• Обычно: *от 5–10 дней*\n"
            "• Фиксированная цена за проект (после короткого брифа)\n"
            "• Включены запуск, короткое обучение и передача\n\n"
            "Точная цена зависит от функций — нажми *Заказать бота*."
        ),
        "contact_me": (
            "*Связаться со мной*\n\n"
            "Telegram: @{username}\n"
            "Телефон / Telegram: {phone}\n"
            "WhatsApp: {whatsapp_url}\n"
            "Город: Вроцлав, Польша\n\n"
            "Или нажми *Заказать бота* и оставь нишу + задачу."
        ),
        "ask_niche": (
            "🚀 *Обсудим вашего бота*\n\n"
            "Какая ниша бизнеса?\n"
            "_(например: салон красоты, клиника, доставка, недвижимость)_"
        ),
        "ask_task": (
            "Понял — *{niche}*.\n\n"
            "Что должен делать бот?\n"
            "_(запись, каталог, сбор заявок с фото и т.д.)_"
        ),
        "ask_contact": (
            "Почти готово.\n\n"
            "Как с вами связаться? Пришлите *телефон* или *@username*."
        ),
        "need_niche": "Напишите нишу коротко (несколько слов).",
        "need_task": "Опишите задачу коротким сообщением.",
        "need_contact": "Пришлите телефон или @username.",
        "thanks": (
            "✅ Спасибо! Заявка получена.\n\n"
            "Ниша: {niche}\n"
            "Задача: {task}\n"
            "Контакт: {contact}\n\n"
            "Скоро отвечу. Также можно написать @{username}."
        ),
        "cancelled": "Остановил. Отправьте /start, чтобы открыть меню.",
        "help": (
            "/start — меню\n"
            "/cancel — отменить заказ"
        ),
    },
    "uk": {
        "welcome": (
            "Привіт! Я створюю Telegram-ботів під ключ для бізнесу "
            "(автоматизація, запис, каталоги, прийом заявок і фото).\n\n"
            "Бот, у якому ти зараз — живий приклад моєї роботи.\n\n"
            "Працюю у *Вроцлаві*. Чим можу допомогти?"
        ),
        "btn_order": "🚀 Замовити бота / Обговорити проєкт",
        "btn_cases": "💼 Приклади та кейси",
        "btn_pricing": "💰 Вартість і строки",
        "btn_contact": "📞 Зв’язатися зі мною",
        "btn_language": "🌐 Мова",
        "btn_back": "⬅️ До меню",
        "cases": (
            "*Приклади та кейси*\n\n"
            "Що вміють боти, які я роблю:\n\n"
            "• *Каталоги* — послуги/товари з фото та цінами\n"
            "• *Воронки заявок* — ніша → задача → контакт\n"
            "• *Запис* — слоти та нагадування\n"
            "• *Багатомовність* — PL / EN / RU / UK\n"
            "• *Інтеграції* — Google Sheets, webhook, оплати, CRM\n"
            "• *Прийом фото* — клієнт надсилає фото задачі\n\n"
            "Цей бот — робоче портфоліо, можна пройти весь сценарій."
        ),
        "pricing": (
            "*Вартість і строки*\n\n"
            "• Зазвичай: *від 5–10 днів*\n"
            "• Фіксована ціна за проєкт (після короткого брифу)\n"
            "• У ціні: запуск, коротке навчання і передача\n\n"
            "Точна ціна залежить від функцій — натисни *Замовити бота*."
        ),
        "contact_me": (
            "*Зв’язатися зі мною*\n\n"
            "Telegram: @{username}\n"
            "Телефон / Telegram: {phone}\n"
            "WhatsApp: {whatsapp_url}\n"
            "Місто: Вроцлав, Польща\n\n"
            "Або натисни *Замовити бота* і залиш нішу + задачу."
        ),
        "ask_niche": (
            "🚀 *Обговоримо вашого бота*\n\n"
            "Яка ніша бізнесу?\n"
            "_(наприклад: салон краси, клініка, доставка, нерухомість)_"
        ),
        "ask_task": (
            "Зрозумів — *{niche}*.\n\n"
            "Що має робити бот?\n"
            "_(запис, каталог, збір заявок з фото тощо)_"
        ),
        "ask_contact": (
            "Майже готово.\n\n"
            "Як з вами зв’язатися? Надішліть *телефон* або *@username*."
        ),
        "need_niche": "Напишіть нішу коротко (кілька слів).",
        "need_task": "Опишіть задачу коротким повідомленням.",
        "need_contact": "Надішліть телефон або @username.",
        "thanks": (
            "✅ Дякую! Заявку отримано.\n\n"
            "Ніша: {niche}\n"
            "Задача: {task}\n"
            "Контакт: {contact}\n\n"
            "Скоро відповім. Також можна написати @{username}."
        ),
        "cancelled": "Зупинив. Надішліть /start, щоб відкрити меню.",
        "help": (
            "/start — меню\n"
            "/cancel — скасувати замовлення"
        ),
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
    lang = lang if lang in TEXTS else DEFAULT_LANG
    template = TEXTS[lang].get(key) or TEXTS[DEFAULT_LANG][key]
    kwargs.setdefault("business_name", BUSINESS_NAME)
    kwargs.setdefault("username", CONTACT_USERNAME)
    kwargs.setdefault("phone", CONTACT_PHONE)
    kwargs.setdefault("whatsapp_url", CONTACT_WHATSAPP_URL)
    return template.format(**kwargs)
