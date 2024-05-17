import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
import calc_handler
from os import getenv

load_dotenv(find_dotenv())

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(getenv('TOKEN'))

    dp.include_router(calc_handler.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())