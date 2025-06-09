from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def support_done_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Связь с поддержкой', callback_data='communication-support')
    return builder.adjust(1).as_markup()


def support_done_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='✅ Вопрос решён')
    return builder.as_markup(resize_keyboard=True)