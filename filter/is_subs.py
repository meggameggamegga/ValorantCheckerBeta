from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Filter

from db.base_db import DataBase
from main import bot

db = DataBase('test.db')


class IsSubs_MSG(Filter):
    async def check(self, message: types.Message) -> bool:
        user = db.get_cur_sub(message.from_user.id)
        if user is None:
            await bot.send_message(message.from_user.id, 'Оплатите подписку')
            return False
        user_id = user[0]
        if int(user_id) == int(message.from_user.id):
            user_time = user[1]
            user_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S.%f")
            current_time = datetime.now()
            time_difference = user_time - current_time
            if time_difference.total_seconds() > 0:
                return True
            else:
                db.delete_pay(message.from_user.id)
                await bot.send_message(message.from_user.id, '❗Ваша подписка закончена\n'
                                                             'Перейдите в меню , что бы оплатить.')
                return False
        else:
            await bot.send_message(message.from_user.id, 'Оплатите подписку')
            return False
