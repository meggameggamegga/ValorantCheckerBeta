from aiogram import types
from aiogram.dispatcher.filters import Filter

from db.base_db import DataBase

db = DataBase('test.db')


class IsAdmin_MSG(Filter):
    async def check(self, message: types.Message) -> bool:
        buyers_ids = db.get_selleres()
        user_id = message.from_user.id
        for buyer in buyers_ids:
            if buyer[1] == user_id:
                return True


class IsAdmin_CALL(Filter):
    async def check(self, call: types.CallbackQuery) -> bool:
        buyers_ids = db.get_selleres()
        user_id = call.message.chat.id
        for buyer in buyers_ids:
            if buyer[1] == user_id:
                return True
