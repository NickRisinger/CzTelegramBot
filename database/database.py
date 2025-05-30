from prisma import Prisma
from prisma.types import UserCreateInput
from prisma.models import User


async def get_user(tg_id: int) -> User:
    async with Prisma() as db:
        return await db.user.find_first(
            where={'tg_id': tg_id},
        )


async def create_user(tg_id: int):
    async with Prisma() as db:
        return await db.user.create(
            data=UserCreateInput(tg_id=tg_id)
        )
