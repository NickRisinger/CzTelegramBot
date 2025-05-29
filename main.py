import asyncio
from prisma import Prisma
from prisma.types import UserCreateInput

async def main():
    db = Prisma()
    await db.connect()

    try:
        user = await db.user.create(
            data=UserCreateInput(tg_id=123456780)
        )

        print(f'Created user: {user.model_dump_json()}')
    except Exception as e:
        print(f'Error: {e}')

    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
