import asyncio
import os
import datetime
import requests
import logging
from aiogram import Bot, Dispatcher
from message_handlers import router
from config import TG_TOKEN

bot = Bot(token=TG_TOKEN)
async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='bot.log')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped!')