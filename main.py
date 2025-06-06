import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config
from utils.utils import load_gtins_from_excel, load_products_from_excel

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.gifts import router as gifts_router
from handlers.support import router as support_router
from handlers.process import router as process_router
from handlers.admin import router as admin_router


logging.basicConfig(level=logging.INFO)


async def startup(dispatcher: Dispatcher):
    try:
        load_gtins_from_excel()
        load_products_from_excel()
    except Exception as e:
        print('Ошибка: ', e)


async def main():
    bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    await bot(DeleteWebhook(drop_pending_updates=True))

    dp.startup.register(startup)

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(gifts_router)
    dp.include_router(support_router)
    dp.include_router(process_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
