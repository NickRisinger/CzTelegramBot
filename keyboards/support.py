from aiogram.utils.keyboard import ReplyKeyboardBuilder

def support_done_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='✅ Вопрос решён')
    return builder.as_markup(resize_keyboard=True)