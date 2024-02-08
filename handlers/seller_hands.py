import datetime
import json
import logging

import time


from aiogram.dispatcher.filters import Command, state

import config
from checker import ClientAcc
from db.base_db import DataBase
from filter.Language_filter import *
from filter.is_admin import *
from filter.is_seller import IsAdmin_MSG, IsAdmin_CALL

from keyboards.inline import auth_menu, cb
from keyboards.inline_lang import cb_settings
from keyboards.sell_acc_keyb import cb_sell_acc
from keyboards.seller_keyb import seller_lk, cb_seller_lk

from main import bot,dp
from states.state import StartState, AdminState, LKSeller
from valo_lib import Auth
from src.screen_skins import image_skins
db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.seller_hands')

#Добавить фильтр для селлеров
@dp.message_handler(IsAdmin_MSG(),Command('seller'))
async def seller_cmnd(message:types.Message):
    logger.info(f'Команда start_cmnd для пользователя {message.from_user.first_name}')
    await message.answer('Привет!',reply_markup=seller_lk())#Клавиатура

@dp.callback_query_handler(IsAdmin_CALL(),cb_seller_lk.filter(action='set_lk'))
async def set_lk_status(call:types.CallbackQuery):
    logger.info(f'Команда set_lk_status для пользователя {call.message.chat.first_name}')
    await call.answer()
    await call.message.answer('📊 Статус сделки:\n'
                              '✅ Успешно - если сделка прошла и клиент продал вам аккаунт\n'
                              '❌ Отмена - если пользователь вам написал, но аккаунт не был куплен.\n'
                              '📝 Пример ввода: <b>статус:ID_аккаунта</b>')

    await LKSeller.set_status_lk.set()

@dp.message_handler(IsAdmin_MSG(),state=LKSeller.set_status_lk)
async def add_status_lk(message:types.Message,state:FSMContext):
    logger.info(f'Команда add_status_lk для пользователя {message.from_user.first_name}')
    status = message.text.split(':')[0]
    label = message.text.split(':')[1]
    buyer_id = db.get_buyer_id(message.from_user.id)
    #Если сделка завершилась гуд
    if status == 'Успешно':
        #Берем все статусы c ID баером
        db.set_status_seller(status,label,buyer_id[0])
        all_label_status = db.get_status_buyer(label)
        #Проходимся по ним
        for label_status in all_label_status:
            if label_status[0] != 'Успешно':
                db.set_status_seller('Отмена',label,label_status[1])

    else:
        db.set_status_seller(status,label,buyer_id[0])
    await message.reply(f'Статус для {label} установлен на {status}')
    await state.reset_state()


@dp.callback_query_handler(IsAdmin_CALL(),cb_seller_lk.filter(action='get_deals'))
async def get_deals_seller(call:types.CallbackQuery):
    pass
