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
