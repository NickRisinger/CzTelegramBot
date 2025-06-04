from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext

from config.config import Config


class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.admins = Config.ADMINS.split(',')

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not event.from_user.id in self.admins:
            return

        return await handler(event, data)