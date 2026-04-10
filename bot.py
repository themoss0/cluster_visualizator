import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from core.di.injection import load_dependencies
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())