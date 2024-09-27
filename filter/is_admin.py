from aiogram import types
from aiogram.dispatcher.filters import Filter

from db.base_db import DataBase

import config

db = DataBase('test.db')

class IsAdmin(Filter):
    key='is_admin'
    async def check(self,message:types.Message) -> bool:
        return True if str(message.from_user.id) == config.ADMIN_ID else False
