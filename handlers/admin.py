from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import IsAdmin
from middlewares.support import SupportMiddleware
from utils.utils import load_products_from_excel, load_gtins_from_excel

router = Router()
router.message.middleware(SupportMiddleware())
router.message.filter(IsAdmin())


@router.message(Command('updateGtins'))
async def cmd_update_gtins(message: Message):
    try:
        load_gtins_from_excel()

        await message.answer('Данные обновлены!')
    except Exception as e:
        await message.answer(f'Ошибка: {e}')


@router.message(Command('updateGifts'))
async def cmd_update_gifts(message: Message):
    try:
        load_products_from_excel()

        await message.answer('Данные обновлены!')
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
