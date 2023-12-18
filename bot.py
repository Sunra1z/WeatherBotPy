import asyncio
import logging

from aiogram import Bot, Dispatcher
from message_handlers import router
from config import TG_TOKEN
from database import async_main

bot = Bot(token=TG_TOKEN)
async def main(): # Main function to run the bot
    await async_main()
    bot = Bot(token=TG_TOKEN) # Create a bot object
    dp = Dispatcher() # Create a dispatcher object
    dp.include_router(router) # Add router to dispatcher (connect to msg handlers)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='bot.log') # logging to a specifi file
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped!')
