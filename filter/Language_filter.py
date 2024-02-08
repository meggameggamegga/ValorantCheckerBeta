from aiogram import types

from aiogram.dispatcher.filters import Filter

from db.base_db import DataBase
from typing import Union
db = DataBase('test.db')


class IsLanguageENG(Filter):
    async def check(self,message:types.Message) -> bool:
        if str(db.get_language(message.from_user.id)) == 'EU':
            return True
        else:
            return False

class IsLanguageENG_CALL(Filter):
    async def check(self,call:types.CallbackQuery) -> bool:
        if str(db.get_language(call.message.chat.id)) == 'EU':
            return True
        else:
            return False

class IsLanguageRU(Filter):
    async def check(self,message:Union[types.Message, types.CallbackQuery]) -> bool:
        if str(db.get_language(message.from_user.id)) == 'RU':
            return True
        else:
            return False

class IsLanguageRU_CALL(Filter):
    async def check(self,call:types.CallbackQuery) -> bool:
        if str(db.get_language(call.message.chat.id)) == 'RU':
            return True
        else:
            return False

