from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import config


class ChannelMiddleware(BaseMiddleware):
    def __init__(self,bot):
        self.bot = bot
        super(ChannelMiddleware,self).__init__()

    async def on_pre_process_message(self,message:types.Message,bot):
        user_group = await self.bot.get_chat_member(config.CHAT_ID,message.from_user.id)
        if user_group['status'] == 'left':
            await message.reply('Подпишись на наш канал https://t.me/checker_valo')
            raise CancelHandler()

    async def on_pre_process_callback_query(self,call:types.CallbackQuery,bot):
        user_group = await self.bot.get_chat_member(config.CHAT_ID, call.message.chat.id)
        if user_group['status'] == 'left':
            await call.message.reply('Подпишись на наш канал https://t.me/checker_valo')
            raise CancelHandler()