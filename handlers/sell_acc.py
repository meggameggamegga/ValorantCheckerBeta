
import json
import logging


from checker import ClientAcc

from filter.is_admin import *

from keyboards.inline import auth_menu, cb

from keyboards.sell_acc_keyb import sell_acc_keyboard, cb_sell_acc, sell_acc_buyer, cb_sell_buyer, sell_acc_client

from main import bot,dp
from states.state import BuyerState

from src.screen_skins import image_skins
import string
import random
db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.sell_acc')

@dp.callback_query_handler(cb.filter(action='sell_acc'))
async def sell_acc_info(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда sell_acc_info для пользователя {call.message.chat.first_name}')
    #Провека,есть ли этот аккаунт в истории как ожидание (статус)
    letters_and_digits = string.ascii_lowercase + string.digits  # Создаем строку с цифрами и буквами
    label = '#' + ''.join(random.sample(letters_and_digits, 5))
    async with state.proxy() as data:
        username = data['username']
        data['label'] = label
    await call.message.edit_text(f'🤖 Как происходит продажа?\n'
                              f'Если вы подтвердите отправку информации:\n'
                              f'🎮 - <b>Скинов</b>\n'
                              f'🌎 - <b>Региона</b>\n'
                              f'🔗 - <b>Привязки</b>\n'
                              f'⚔ - <b>Крайнего матча</b>\n'
    f'То бот предложит вам цену, за которую вы можете продать аккаунт.\n'
    f'Отправить информацию об аккаунте <b>{username}?</b>\n\n'
    f'<b>❗ВАЖНО❗\n</b>'
    f'<b>-Аккаунт должен быть с почтой (атворег и тп.) или с неподтвержденной почтой\n</b>',reply_markup = sell_acc_keyboard())

@dp.callback_query_handler(cb_sell_acc.filter(action='send_acc'))
async def sell_acc_send_buy(call:types.CallbackQuery,state:FSMContext):
    await call.answer()
    logger.info(f'Команда sell_acc_send_buy для пользователя {call.message.chat.first_name}')
    async with state.proxy() as data:
        username = data['username']
        password = data['password']
        ent_token = data['entitlements_token']
        acc_token = data['access_token']
        region = data['region']
        puuid = data['puuid']
        label = data['label']
        phone_verif = data["verif_phone"]
        mail_verif = data['verif_mail']
    client = ClientAcc(username=username,password=password)
    if not client:
        cur_state = await state.get_state()
        if cur_state:
            await state.reset_state()
        await call.message.reply('Похоже данные от аккаунта поменялись',reply_markup=auth_menu('Auth'))
    else:
        items = client.get_items(item='e7c63390-eda7-46e0-bb7a-a6abdacd2433',
                                 ent_token=ent_token,
                                 region=region,
                                 acc_token=acc_token,
                                 puuid=puuid)
        accounts = client.get_my_account(ent_token=ent_token,
                                         region=region,
                                         acc_token=acc_token,
                                         puuid=puuid)

        with open('purchasableSkins.json', 'r') as file:
            prices = json.load(file)
        # ID всех скинов
        with open('skins_data.json', 'r', encoding='UTF8') as skins_file:
            skins_data = json.load(skins_file)
        sum_skin = 0
        price_skin = {}
        skin_full = {}
        for skin_id in items['Entitlements']:
            for skin_uuid in skins_data['data']:
                if skin_id['ItemID'] == skin_uuid['uuid']:
                    if not 'уровень' in skin_uuid['displayName']:
                        skin_full[skin_uuid['displayName']] = skin_uuid['uuid']
                        for price in prices['data']:
                            if price['uuid'] == skin_uuid['uuid']:
                                price_skin[skin_uuid['displayName']] = price['vpCost']
        if not skin_full:
            await call.message.delete()
            await call.message.answer('<b>Скинов на аккаунте нет.</b>',reply_markup=auth_menu('Login'))
        else:
            for skin, price in price_skin.items():
                sum_skin += int(price)
            print(sum_skin)
            await call.message.delete()
            await call.message.answer(f'📊 <b>Информация об аккаунте {username} успешно отправлена!</b>\n'
                                      f'🆔 Аккаунт ID: <b>{label}</b>')
            #Отправляем всем селлерам
            sellers = db.get_selleres()
            for seller in sellers:
                urls_photo = image_skins(skin_full,lang='RU')
                #Тут проверить что бы ID юзера селлра добавилось
                db.add_account(user_id=call.message.chat.id,label=label,login=username,password=password,status='Ожидание',buyer_id=seller[0])
                for photo in urls_photo:
                    await bot.send_photo(chat_id=int(seller[1]),
                                     photo=types.InputFile(photo))
            if accounts['Rank'] is None:
                if phone_verif == False:
                    phone_verif = '❌'
                else:
                    phone_verif = '✅'
                if mail_verif == False:
                    mail_verif = '❌'
                else:
                    mail_verif = '✅'
                last_match = accounts['last_match']
                sellers = db.get_selleres()
                for seller in sellers:
                    await bot.send_message(chat_id=int(seller[1]),text=f'Информация об аккаунте\n'
                                             f'🌟Ранг:Unranked\n'
                                             f'🌍Регион: <b>{region}</b>\n'
                                             f'🏆Крайний матч:<b>{last_match}</b>\n'
                                             f'💰Сумма скинов: {sum_skin}VP\n'
                                             f'📧Почта:{mail_verif}\n'
                                             f'📞Телефон:{phone_verif}\n'
                                             f'📧Аккаунт ID: <b>{label}</b>'
                                             ,reply_markup=sell_acc_buyer(call.message.chat.id,label))
            else:
                if phone_verif == False:
                    phone_verif = '❌'
                else:
                    phone_verif = '✅'
                if mail_verif == False:
                    mail_verif = '❌'
                else:
                    mail_verif = '✅'
                rank = config.ranks[accounts['Rank']]
                sellers = db.get_selleres()
                last_match = accounts['last_match']
                for seller in sellers:
                    await bot.send_message(chat_id=int(seller[1]), text=f'🌍 Регион: <b>{region}</b>\n'
                                                                        f'🌟 Ранг: <b>{rank}</b>\n'
                                                                        f'💰 Сумма скинов: {sum_skin}VP\n'
                                                                        f'🏆 Крайний матч:<b>{last_match}</b>\n'
                                                                        f'📞 Телефон: {phone_verif}\n'
                                                                        f'📧 Почта: {mail_verif}'
                                                                        f'Аккаунт ID: <b>{label}</b>',reply_markup=sell_acc_buyer(call.message.chat.id, label))


@dp.callback_query_handler(cb_sell_buyer.filter(action='send_price'),state='*')
async def choose_price_to_user(call:types.CallbackQuery,state:FSMContext,callback_data:dict):
    logger.info(f'Команда choose_price_to_user для пользователя {call.message.chat.first_name}')
    await call.answer()
    async with state.proxy() as data:
        data['client_id'] = callback_data.get('client_id')
        data['label'] = callback_data.get('label')
    label = callback_data.get('label')
    buyer_id = db.get_buyer_id(call.message.chat.id)
    statuses_deals = db.get_cur_status(label,buyer_id[0])[0]
    if statuses_deals == 'Отмена':
        await call.message.delete()
        await call.message.answer(f'Аккаунт <b>{label}</b> уже не актуален')
        await state.reset_state()
    elif statuses_deals == 'Успешно':
        await call.message.delete()
        await call.message.answer(f'Вы уже продали аккаунт <b>{label}</b>!')
        await state.reset_state()
    else:
        await call.message.answer(f'💰 Введите сумму в рублях, которую вы готовы заплатить за аккаунт <b>{label}</b>:\n')
        await BuyerState.send_price.set()

@dp.message_handler(state=BuyerState.send_price)
async def send_price_user(message:types.Message,state:FSMContext):
    logger.info(f'Команда send_price_user для пользователя {message.from_user.first_name}')
    buyer_id = db.get_buyer_id(message.from_user.id)
    async with state.proxy() as data:
        label = data['label']
        client_id = data['client_id']
    await bot.send_message(chat_id=client_id, text=f'🆔 <b>Аккаунт ID:</b> {label}\n'
                                                   f'👥 Баер #{buyer_id[0]}\n'
                                                   f'💲 Цена: {message.text} рублей\n'
                                                   f'🆔 Не забудьте предоставить ID!\n'
                                                   f'🌟 Удачной продажи!',reply_markup=sell_acc_client(message.from_user.username))

    db.add_account_price(user_id=client_id,label=label,price_buyer=message.text,
                         buyer_id=buyer_id[0])
    db.set_status(client_id,label,status='Отправлено',buyer_id=buyer_id[0])
    await message.answer(f'💰 Цена отправлена пользователю!\n'
                         f'🆔 <b>Аккаунт ID:</b> {label}\n')

    await state.reset_state()


@dp.callback_query_handler(cb_sell_buyer.filter(action='cancel_price'),state='*')
async def cancle_price_to_user(call:types.CallbackQuery,state:FSMContext,callback_data:dict):
    logger.info(f'Команда cancle_price_to_user для пользователя {call.message.chat.first_name}')
    print(callback_data)
    async with state.proxy() as data:
        label = callback_data.get('label')
        client_id = callback_data.get('client_id')
    buyer_id = db.get_buyer_id(user_id=call.message.chat.id)[0]
    db.set_status(client_id,label,'Отмена',buyer_id)
    await call.message.delete()
    await call.message.answer(f'❌ Вы отказались от покупки аккаунта {label}')

