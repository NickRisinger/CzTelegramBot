from aiogram import Router, F
from prisma import Prisma
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from prisma.types import UserCreateInput
from prisma.models import User

router = Router()


# ============================

async def get_user(tg_id: int) -> User:
    async with Prisma() as db:
        return await db.user.find_first(
            where={"tg_id": tg_id},
        )


async def create_user(tg_id: int):
    async with Prisma() as db:
        return await db.user.create(
            data=UserCreateInput(tg_id=tg_id)
        )


from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def yes_no_keyboard(prefix: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data=f'{prefix}:yes')
    builder.button(text='Нет', callback_data=f'{prefix}:no')
    return builder.as_markup()


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Профиль')
    builder.button(text='Сканировать код')
    builder.button(text='Выбрать подарки')
    builder.button(text='Правила акции')
    builder.button(text='Связь с поддержкой')

    return builder.adjust(1).as_markup(resize_keyboard=True)


# ============================

start_message = ('Благодарим за участие в Акции!\n'
                 'Давайте сканировать коды.\n\n'
                 '<b>Профиль</b> - \n'
                 '<b>Сканировать код</b> - \n'
                 '<b>Выбрать подарки</b> - \n'
                 '<b>Правила акции</b> - \n'
                 '<b>Связь с поддержкой</b> - \n')

unconfirmed_message = ('Извините, вы не можете учавствовать в акции!\n'
                       'Для повторной регистрации напишите команду /start')


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await get_user(message.from_user.id)

    if user is None:
        await message.answer(
            'Согласны ли вы с условием проведения Акции <a href="https://mjolnir-podarkivsem.ru/">"Подарки для всех"</a>',
            reply_markup=yes_no_keyboard('policy'))
        return

    await message.answer(
        start_message,
        reply_markup=main_menu_keyboard())


@router.callback_query(F.data.startswith('policy'))
async def process_policy(callback: CallbackQuery):
    answer = callback.data.split(':')[1]

    await callback.message.edit_reply_markup(None)

    if answer == 'no':
        await callback.message.answer(
            unconfirmed_message,
            reply_markup=None
        )
        return

    await callback.message.answer('Вам есть 18 лет?', reply_markup=yes_no_keyboard('age'))


@router.callback_query(F.data.startswith('age'))
async def process_age(callback: CallbackQuery):
    answer = callback.data.split(':')[1]

    await callback.message.edit_reply_markup(None)

    if answer == 'no':
        await callback.message.answer(
            unconfirmed_message,
            reply_markup=None
        )
        return

    await create_user(callback.from_user.id)

    await callback.message.answer(
        start_message,
        reply_markup=main_menu_keyboard())
