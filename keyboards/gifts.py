from aiogram.utils.keyboard import InlineKeyboardBuilder


def products_keyboard(products: dict):
    builder = InlineKeyboardBuilder()

    for pid, product in products.items():
        builder.button(text=f'{product["name"]} - {product["price"]}', callback_data=f'view:{pid}')

    return builder.adjust(1).as_markup(resize_keyboard=True)


def product_keyboard(id, price):
    builder = InlineKeyboardBuilder()

    builder.button(text='Назад', callback_data=f'back')
    builder.button(text=f'Обменять за {price} балов', callback_data=f'buy:{id}')

    return builder.adjust(2).as_markup(resize_keyboard=True)
