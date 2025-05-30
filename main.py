import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties

from config.config import Config

from handlers.start import router as start_router
from handlers.profile import router as profile_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await bot(DeleteWebhook(drop_pending_updates=True))

    dp.include_router(start_router)
    dp.include_router(profile_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
