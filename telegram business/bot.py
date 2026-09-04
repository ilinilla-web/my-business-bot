"""aiogram Bot and Dispatcher.

Imported by main.py. Do not run this file directly — use:

    python main.py
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, configure_logging
from handlers import setup_routers

configure_logging()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
setup_routers(dp)
