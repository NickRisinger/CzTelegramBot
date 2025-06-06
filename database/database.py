from prisma import Prisma
from prisma.types import UserCreateInput, TreadCreateInput, CodeCreateInput
from prisma.models import User, Tread, Code


async def get_user(tg_id: int) -> User:
    async with Prisma() as db:
        return await db.user.find_first(
            where={'tg_id': tg_id},
        )


async def get_user_and_codes(tg_id: int) -> User:
    async with Prisma() as db:
        return await db.user.find_first(
            where={'tg_id': tg_id},
            include={'codes': True}
        )


async def update_balance(tg_id, points):
    async with Prisma() as db:
        return await db.user.update(
            where={'tg_id': tg_id},
            data={'points': {'decrement': points}},
        )


async def create_user(tg_id: int):
    async with Prisma() as db:
        return await db.user.create(
            data=UserCreateInput(tg_id=tg_id)
        )


async def create_tread(tg_id: int, tread_id: int):
    async with Prisma() as db:
        return await db.tread.create(
            data=TreadCreateInput(user_tg_id=tg_id, tread_id=tread_id)
        )


async def get_tread(tread_id: int) -> Tread:
    async with Prisma() as db:
        return await db.tread.find_first(
            where={'tread_id': tread_id},
        )


async def add_code(tg_id: int, code: str):
    async with Prisma() as db:
        async with db.tx() as transaction:
            await transaction.code.create(
                data=CodeCreateInput(content=code, user_tg_id=tg_id)
            )

            await transaction.user.update(
                where={'tg_id': tg_id},
                data={'points': {'increment': 1}},
            )


async def get_code(code: str) -> Code:
    async with Prisma() as db:
        return await db.code.find_first(
            where={'content': code},
        )
