from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database.database import get_user, create_user
from keyboards.start import yes_no_keyboard, main_menu_keyboard

router = Router()

start_message = ('Благодарим за участие в Акции!\n'
                 'Давайте сканировать коды.\n\n'
                 '<b>Навигация в меню:</b>\n'
                 '<b>Профиль</b> - здесь вы можете посмотреть общую информацию о вашем профиле.\n'
                 '<b>Сканировать код</b> - присылайте фото ваших кодов.\n'
                 '<b>Выбрать подарки</b> - здесь можно посмотреть подарки и выбрать приз себе по душе.\n'
                 '<b>Правила акции</b> - файл с правилами акции.\n'
                 '<b>Связь с поддержкой</b> - здесь мы поможем решить ваши вопросы.\n')

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
