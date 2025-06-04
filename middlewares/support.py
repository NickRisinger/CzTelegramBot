from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from handlers.support import SupportState


class SupportMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        context: FSMContext = data.get('state')

        if context:
            state = await context.get_state()

            if state == SupportState.in_support:
                await event.answer("Вы сейчас общаетесь с поддержкой. Завершите диалог, чтобы использовать бота.")
                return

        return await handler(event, data)