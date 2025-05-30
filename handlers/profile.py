from aiogram import Router, F
from aiogram.types import Message, FSInputFile
# from database.database import get_user, create_user
from prisma import Prisma
from prisma.models import User

from utils.utils import format_date

router = Router()


async def get_user(tg_id: int) -> User:
    async with Prisma() as db:
        return await db.user.find_first(
            where={'tg_id': tg_id},
            include={'codes': True}
        )


@router.message(F.text == 'Профиль')
async def profile_handler(message: Message):
    user = await get_user(message.chat.id)

    profile_text = (
        f"👤 <b>Профиль пользователя</b>\n\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"👤 Username: @{message.from_user.username}\n"
        f"⭐️ Остаток кодов: {user.points}\n"
        f"🎟 Все коды: {len(user.codes)}\n"
        f"📅 Дата регистрации: {format_date(str(user.created_at))}"
    )

    await message.answer(profile_text)


@router.message(F.text == 'Правила акции')
async def promotion_rules(message: Message):
    text = (
        "📜 <b>Правила акции:</b>\n\n"
        "1. Обменивайте баллы на подарки.\n"
        "2. Алкогольные подарки доступны только совершеннолетним.\n"
        "3. Подробности в прикреплённом PDF-файле."
    )
    pdf = FSInputFile("./data/rules.pdf")

    await message.answer(text)
    await message.answer_document(document=pdf)
