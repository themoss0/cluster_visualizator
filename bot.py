import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в переменных окружения")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


# import os
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher
# from core.di.injection import load_dependencies
# from handlers import register_handlers

# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
# register_handlers(dp)

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())