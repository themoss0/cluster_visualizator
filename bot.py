import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
import config   # config.py в той же папке
from core.di.injection import load_dependencies
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())