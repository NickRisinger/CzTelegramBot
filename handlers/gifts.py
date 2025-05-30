from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.gifts import products_keyboard, product_keyboard
from keyboards.start import yes_no_keyboard
from utils.utils import products

router = Router()

GIFTS = {
    "gift1": {
        "name": "Вино красное",
        "price": 150,
        "description": "Хорошее вино из Франции",
        "alcohol": True
    },
    "gift2": {
        "name": "Плюшевая игрушка",
        "price": 70,
        "description": "Мягкая игрушка для детей",
        "alcohol": False
    },
    "gift3": {
        "name": "Шоколадный набор",
        "price": 90,
        "description": "Набор из 5 видов шоколада",
        "alcohol": False
    }
}


class GiftState(StatesGroup):
    choosing_gift = State()
    viewing_gift = State()
    confirm_purchase = State()
    entering_fio = State()
    entering_address = State()
    entering_phone = State()


@router.message(F.text == 'Выбрать подарки')
async def gifts_handler(message: Message, state: FSMContext):
    await message.answer('Доступные продукты', reply_markup=products_keyboard(GIFTS))
    await state.set_state(GiftState.choosing_gift)
    print('TEST', message.chat.id)


@router.callback_query(F.data.startswith('view'))
async def gift_handler(callback: CallbackQuery, state: FSMContext):
    gift_id = callback.data.split(':')[1]
    # product = products.get(gift_id)
    gift = GIFTS[gift_id]
    await state.update_data(gift_id=gift_id)

    await callback.message.delete()

    text = (
        f"<b>{gift['name']}</b>\n"
        f"{gift['description']}\n\n"
        f"Стоимость: {gift['price']} баллов\n"
        f"{'🍷 Алкогольный' if gift['alcohol'] else '🚫 Безалкогольный'}"
    )

    await callback.message.answer(text, reply_markup=product_keyboard(gift_id, gift['price']))


@router.callback_query(F.data.startswith('back'))
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await gifts_handler(callback.message, state)


@router.callback_query(F.data.startswith('buy'))
async def buy_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gift = GIFTS[data["gift_id"]]

    await callback.message.delete()

    await callback.message.answer(
        f'Вы уверены что хотите обменять {gift['price']} на {gift['name']}? Баллы сгорают. Изменить свой выбор нельзя.',
        reply_markup=yes_no_keyboard(f'approval')
    )


@router.callback_query(F.data.startswith('approval'))
async def back_handler(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split(':')[1]
    data = await state.get_data()
    gift = GIFTS[data["gift_id"]]

    if answer == 'no':
        await gifts_handler(callback.message)
        return

    if gift["alcohol"]:
        await callback.message.edit_text("Введите ФИО:")
        await state.set_state(GiftState.entering_fio)
    else:
        await callback.message.edit_text("Введите адрес доставки:")
        await state.set_state(GiftState.entering_address)


@router.message(GiftState.entering_fio)
async def get_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите адрес доставки:")
    await state.set_state(GiftState.entering_address)


@router.message(GiftState.entering_address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(GiftState.entering_phone)


@router.message(GiftState.entering_phone)
async def get_phone(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    gift = GIFTS[data["gift_id"]]

    order_info = (
        f"🎁 <b>Новый заказ</b>\n\n"
        f"Подарок: {gift['name']}\n"
        f"Username: @{message.from_user.username}\n"
        f"ФИО: {data.get('fio', '—')}\n"
        f"Адрес: {data['address']}\n"
        f"Телефон: {data['phone']}\n"
        f"Тип: {'🍷 Алкогольный' if gift['alcohol'] else '🚫 Безалкогольный'}"
    )

    await bot.send_message(chat_id=6435546391, text=order_info)
    await message.answer("✅ Ваш заказ принят!")
    await state.clear()
