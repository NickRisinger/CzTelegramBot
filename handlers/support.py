from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config.config import Config
from database.database import create_tread, get_tread
from keyboards.start import main_menu_keyboard
from keyboards.support import support_done_keyboard
from middlewares.auth import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


# --- Состояния ---
class SupportState(StatesGroup):
    set_subject = State()
    in_support = State()


# --- Кнопка 'Связь с поддержкой' ---
@router.message(F.text == 'Связь с поддержкой')
async def support_start(message: Message, state: FSMContext):
    await state.set_state(SupportState.set_subject)

    await message.answer('Напишите тему вашего обращения, чтоб мы могли быстрее вам помочь.', reply_markup=None)


@router.message(SupportState.set_subject)
async def handle_topic_input(message: Message, bot: Bot, state: FSMContext):
    topic_title = message.text
    user = message.from_user

    topic = await bot.create_forum_topic(
        chat_id=Config.BOT_SUPPORT_GROUP_ID,
        name=topic_title
    )
    thread_id = topic.message_thread_id

    await create_tread(user.id, thread_id)

    await state.set_state(SupportState.in_support)
    await state.update_data(thread_id=thread_id)

    await bot.send_message(
        chat_id=Config.BOT_SUPPORT_GROUP_ID,
        message_thread_id=thread_id,
        text=(f'🆕 Новый запрос от пользователя: @{user.username or user.full_name} (ID: {user.id})\n'
              f'Тема обращения: {topic_title}')
    )

    await message.answer(
        'Вы подключены к оператору поддержки. Можете описать подробнее вашу проблему.\n\n'
        'Когда вопрос будет решён, нажмите кнопку на клавиатуре.',
        reply_markup=support_done_keyboard()
    )


# --- Завершение поддержки ---
@router.message(F.text == '✅ Вопрос решён')
async def end_support(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    thread_id = data['thread_id']

    # Архивируем топик
    # await bot.close_forum_topic(chat_id=Config.BOT_SUPPORT_GROUP_ID, message_thread_id=thread_id)
    await bot.delete_forum_topic(chat_id=Config.BOT_SUPPORT_GROUP_ID, message_thread_id=thread_id)

    # Удаляем состояние
    await state.clear()

    await message.answer('Спасибо, что обратились в поддержку ✅', reply_markup=main_menu_keyboard())


# --- Получение сообщений от пользователя в режиме поддержки ---
@router.message(SupportState.in_support)
async def user_message_to_support(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    thread_id = data['thread_id']

    if message.document:
        await bot.send_document(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            document=message.document.file_id,
            caption=message.caption,
            message_thread_id=thread_id,
        )

    elif message.photo:
        await bot.send_photo(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            photo=message.photo[-1].file_id,
            caption=message.caption,
            message_thread_id=thread_id,
        )

    elif message.video:
        await bot.send_video(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            video=message.video.file_id,
            caption=message.caption,
            message_thread_id=thread_id,
        )

    elif message.voice:
        await bot.send_voice(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            voice=message.voice.file_id,
            caption=message.caption,
            message_thread_id=thread_id,
        )

    elif message.audio:
        await bot.send_audio(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            audio=message.audio.file_id,
            caption=message.caption,
            message_thread_id=thread_id,
        )

    elif message.text:
        await bot.send_message(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            message_thread_id=thread_id,
            text=f'📨 Сообщение от @{message.from_user.username or message.from_user.full_name}:\n\n{message.text}'
        )


# --- Получение сообщений из топика и пересылка пользователю ---
@router.message(F.is_topic_message)
async def support_reply_to_user(message: Message, bot: Bot):
    if message.from_user.is_bot:
        return

    thread_id = message.message_thread_id
    thread = await get_tread(thread_id)

    if message.document:
        await bot.send_document(
            chat_id=thread.user_tg_id,
            document=message.document.file_id,
            caption=message.caption,
        )

    elif message.photo:
        await bot.send_photo(
            chat_id=thread.user_tg_id,
            photo=message.photo[-1].file_id,
            caption=message.caption,
        )

    elif message.video:
        await bot.send_video(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            video=message.video.file_id,
            caption=message.caption,
        )

    elif message.voice:
        await bot.send_voice(
            chat_id=Config.BOT_SUPPORT_GROUP_ID,
            voice=message.voice.file_id,
            caption=message.caption,
        )

    elif message.audio:
        await bot.send_audio(
            chat_id=thread.user_tg_id,
            audio=message.audio.file_id,
            caption=message.caption,
        )

    elif message.text:
        await bot.send_message(
            chat_id=thread.user_tg_id,
            text=f'💬 Поддержка:\n\n{message.text}'
        )


# --- Блокировка остальных кнопок в режиме поддержки ---
@router.callback_query(SupportState.in_support)
async def block_other_buttons(callback: CallbackQuery):
    await callback.answer('Сейчас вы общаетесь с поддержкой. Завершите диалог, чтобы продолжить.', show_alert=True)
