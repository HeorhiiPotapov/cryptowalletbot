import logging

from aiogram import Bot, Dispatcher
from config import BOT_API
from database import Database
from handlers.admin.admin_panel import adminpanel
from handlers.client import start, check_wallet
from handlers.admin import user_confirm, admin_panel
import asyncio


async def main():
    bot = Bot(token=BOT_API)
    dp = Dispatcher()
    Database.init()
    dp.include_routers(
        start.router,
        check_wallet.router,
        user_confirm.router,
        admin_panel.router
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())