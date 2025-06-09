from aiogram.types import Message
from aiogram.filters import Filter
from config.config import Config


class IsAdmin(Filter):
    def __init__(self):
        self.admins = Config.ADMINS.split(',')

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
