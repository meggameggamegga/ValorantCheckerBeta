import asyncio
import json
import logging
import time
from datetime import datetime, timedelta

from aiogram.dispatcher.filters import Command

import config
from filter.Language_filter import *
from filter.is_admin import *
from keyboards.inline import auth_menu, cb
from main import bot,dp
from states.state import AdminState, AddSeller, AddPayCheck, AddTestCheck

db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.admin_panel')

@dp.message_handler(Command('admin_panel'),IsAdmin())
async def admin_start(message:types.Message):
    await message.answer('Привет',reply_markup=auth_menu('Admin'))#admin_menu


MAX_USERS_PER_MESSAGE = 20


@dp.callback_query_handler(cb.filter(action='check_users'))
async def get_all_users(call: types.CallbackQuery):
    logger.info(f'Команда query_all_users для пользователя {call.message.chat.first_name}')

    users = db.get_users()

    # Разбиваем список пользователей на части по MAX_USERS_PER_MESSAGE
    user_chunks = [users[i:i + MAX_USERS_PER_MESSAGE] for i in range(0, len(users), MAX_USERS_PER_MESSAGE)]

    for chunk in user_chunks:
        answer_text = 'Пользователи\n\n'
        for user in chunk:
            answer_text += f'{str(user[0])} - {str(user[1])} - {str(user[2])}\n'

        # Создаем инлайн-клавиатуру для перелистывания пользовате

        await call.message.answer(answer_text)

@dp.callback_query_handler(cb.filter(action='send_messages'),IsAdmin())
async def get_send_messages(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда get_send_messages для пользователя {call.message.chat.first_name}')
    await call.answer()
    await call.message.answer('Введи какой сообщение хочешь отправить')
    await AdminState.message.set()


@dp.message_handler(IsAdmin(),state=AdminState.message.state)
async def accept_message(message:types.Message,state:FSMContext):
    logger.info(f'Команда accept_msg для пользователя {message.from_user.first_name}')
    async with state.proxy() as data:
        data['message'] = message.text
    await message.answer('Пришлите фото')
    await AdminState.photo.set()

@dp.message_handler(IsAdmin(),state=AdminState.photo.state,content_types=types.ContentTypes.PHOTO)
async def get_photo_sender(message:types.Message,state:FSMContext):
    media = message['photo'][-1]['file_id']
    async with state.proxy() as data:
        message_sender = data['message']
        data['photo'] = media
    #await bot.send_video(chat_id=config.ADMIN_ID,video=video,caption=f'Вы уверен что хотите сделать рассылку с таким сообщением\n'
    #                    f'{message_sender}',reply_markup=auth_menu('messages'))
    await bot.send_photo(chat_id=config.ADMIN_ID,photo=media,caption=f'Вы уверен что хотите сделать рассылку с таким сообщением\n'
                        f'{message_sender}',reply_markup=auth_menu('messages'))
    await AdminState.accept.set()

@dp.callback_query_handler(IsAdmin(), cb.filter(action='yes'), state=AdminState.accept.state)
async def send_message(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        message = data['message']
        media = data['photo']
    good_count = 0
    block = 0
    await call.answer()
    users = db.get_users()
    message_id_edit = await bot.send_message(chat_id=config.ADMIN_ID,text=f'Кол-во пользователей {len(users)}\n'
                              f'Отправлено 0\n'
                              f'Блок 0\n')
    for user in users:
        await asyncio.sleep(2)
        try:
            #await bot.send_message(chat_id=int(user[1]), text=f'{message}')
            #await bot.send_video(chat_id=int(user[1]),video=media,caption=f'{message}')
            await bot.send_photo(chat_id=int(user[1]),photo=media,caption=f'{message}')
            good_count += 1
            await bot.edit_message_text(chat_id=config.ADMIN_ID, message_id=message_id_edit.message_id,
                                        text=f'Кол-во пользователей {len(users)}\n'
                                             f'Отправлено {good_count}\n'
                                             f'Блок {block}\n')

            #await bot.send_message(chat_id=config.ADMIN_ID,
            #                           text=f'Рассылка отправлена пользователю {user[1]},{str(user[2])}')  # user[2]

        except Exception as e:
            print(e,f'{int(user[1])}')
            block+=1
            await bot.edit_message_text(chat_id=config.ADMIN_ID,message_id=message_id_edit.message_id,text=f'Кол-во пользователей {len(users)}\n'
                              f'Отправлено {good_count}\n'
                              f'Блок {block}\n')
            #await bot.send_message(chat_id=config.ADMIN_ID, text=f'Пользователь {user[1],{str(user[2])}} заблокировал бота')
    await bot.edit_message_text(chat_id=config.ADMIN_ID,message_id=message_id_edit.message_id,text='Рассылка завершена\n'
                                                                                                   f'Отправил {good_count}\n'
                                                                                                   f'В блоке {block}\n')
    await state.reset_state()

@dp.callback_query_handler(IsAdmin(),cb.filter(action='no'),state=AdminState.accept.state)
async def not_send_message(call:types.CallbackQuery,state:FSMContext):
    await state.reset_state()
    await call.message.answer('Рассылка отменена')
#------------------------Добавить селлера-----------------------#
@dp.callback_query_handler(IsAdmin(),cb.filter(action='add_seller'))
async def add_new_seller(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите user_id селлера:')
    await AddSeller.get_id.set()

@dp.message_handler(IsAdmin(),state=AddSeller.get_id)
async def add_id_seller(message:types.Message,state:FSMContext):
    user_exists = db.user_exist(int(message.text))
    print(user_exists)
    if user_exists:
        db.set_seller(int(message.text),2)
        await message.answer('Пользователь теперь seller')
        await state.reset_state()
    else:
        print('Попал')
        await message.answer('Пользователя нет в боте')
        await state.reset_state()
#--------------------------#


#----------------УДАЛИТЬ СЕЛЛЕРА------------------#
'''
    Вывести список всех селлеров и удалять
'''
@dp.callback_query_handler(IsAdmin(),cb.filter(action='delete_seller'))
async def delete_new_seller(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите user_id селлера:')
    await AddSeller.delete_sell.set()

@dp.message_handler(IsAdmin(),state=AddSeller.delete_sell)
async def delete_id_seller(message:types.Message,state:FSMContext):
    user_exists = db.user_exist(int(message.text))
    if user_exists:
        db.set_seller(int(message.text),0)
        await message.answer('Пользователь теперь обычный юзер')
        await state.reset_state()
    else:
        await message.answer('Пользователя нет в боте')
        await state.reset_state()
#----------------------------#


#---------------Добавление платежа оплаты---------------------#
@dp.callback_query_handler(cb.filter(action='add_to_check'))
async def add_to_more_check(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите user_id пользователя , который оплатил.')
    await AddPayCheck.get_user_id.set()

@dp.message_handler(state=AddPayCheck.get_user_id)
async def add_user_id_check(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['user_id'] = int(message.text)
    await message.answer('Пришлите фото оплаты')
    await AddPayCheck.get_photo_pay.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO,state=AddPayCheck.get_photo_pay)
async def add_photo_check_db(message:types.Message,state:FSMContext):
    photo_file = message['photo'][-1]['file_id']
    async with state.proxy() as data:
        user_id = data['user_id']
    current_time = datetime.now()
    timepay = current_time + timedelta(days=30)
    db.add_user_pay(user_id,photo_file,timepay)
    await message.answer('Пользователь добавлен!')
    await state.reset_state()


#--------------Добавление пробного теста массового чека------------------#
@dp.callback_query_handler(IsAdmin(),cb.filter(action='add_test_check'))
async def add_test_check(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите юзер ID и время в минутах\n'
                              'Формат user_id:time\n')
    await AddTestCheck.get_user_test_id.set()


@dp.message_handler(IsAdmin(),state=AddTestCheck.get_user_test_id)
async def add_test_user(message:types.Message,state:FSMContext):
    msg = message.text.split(':')
    async with state.proxy() as data:
        data['user_id'] = msg[0]
        data['time_min'] = msg[1]
    await message.answer('Пришлите фото')
    await AddTestCheck.get_photo_test.set()

@dp.message_handler(IsAdmin(),content_types=types.ContentTypes.PHOTO,state=AddTestCheck.get_photo_test)
async def add_test_check_photo(message:types.Message,state:FSMContext):
    photo_id = message['photo'][-1]['file_id']
    async with state.proxy() as data:
        user_id = data['user_id']
        time_min = int(data['time_min'])
    time_delta= datetime.now() + timedelta(minutes=time_min)
    db.add_user_pay(user_id,photo_id,time_delta)
    await message.answer(f'Успешно установленно до {time_delta}')
    await state.reset_state()