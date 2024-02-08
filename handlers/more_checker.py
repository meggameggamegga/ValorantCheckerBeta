
import logging
import random

from filter.is_admin import *
from filter.is_subs import IsSubs_MSG
from keyboards.inline import cb, pay_check, admin_pay_accept, cb_pay, auth_menu
from main import bot,dp
from src.for_more_check import get_proxy, get_skins
from states.state import Check, PayCheck
from valo_lib_more import *
from aiohttp import ClientHttpProxyError, ContentTypeError

db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

logger = logging.getLogger('app.more_checker')

@dp.callback_query_handler(cb.filter(action='pay_check'))
async def pay_for_check(call:types.CallbackQuery):
    logger.info(f'Команда pay_for_check для пользователя {call.message.chat.first_name}')
    await call.answer()
    await call.message.edit_text(text=f"<b>Подписка 'Массовый чек' на месяц</b>\n\n"
                                f"💰 Стоимость: 250 рублей\n"
                                
                                f"-------------------------------------\n"
                            
                                f"💳 <b>Способы оплаты:</b>\n"
                                f"<b>LOLZ</b>- <a href='https://zelenka.guru/members/4449624/'>Перевод по профилю</a> - 7% комиссии\n"
                                f"<b>Crypto USDTtrc20</b> - TSduBdzNLwiy2RZBmfq3ARvBkJi1uGYezC\n"
                                f"<b>QIWI</b> - https://qiwi.com/n/MEGAMEGA\n\n"
                                f"📩 Если вам нужен перевод по карте, пишите в личные сообщения.\n",reply_markup=pay_check(),disable_web_page_preview=True)

@dp.callback_query_handler(cb.filter(action='cancel_pay'))
async def cancel_pay_photo(call:types.CallbackQuery):
    logger.info(f'Команда cancel_pay_photo для пользователя {call.message.chat.first_name}')
    await call.answer()
    welcome_message = (
        f'👋 Добро пожаловать, {call.message.from_user.first_name}!\n'
        f'Я бот-чекер игры Valorant. Воспользуйтесь доступными командами для проверки своей коллекции скинов и другой информации. '
        f'Для начала работы нажмите кнопку "Войти".'
    )
    await call.message.edit_text(text=welcome_message,reply_markup=auth_menu('Login'))


@dp.callback_query_handler(cb.filter(action='send_pay'))
async def get_pay_photo(call:types.CallbackQuery,state:FSMContext):
    logger.info(f'Команда get_pay_photo для пользователя {call.message.chat.first_name}')
    await call.answer()
    await call.message.edit_text('Пришлите фото перевода',reply_markup=auth_menu())
    await PayCheck.get_photo.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO,state=PayCheck.get_photo)
async def send_pay_photo(message:types.Message,state:FSMContext):
    logger.info(f'Команда send_pay_photo для пользователя {message.from_user.first_name}')
    photo_user = message['photo'][-1]['file_id']
    await message.answer('<b>Вам придет сообщение о подтверждении оплаты</b>\n')
    client_id = message.from_user.id
    await bot.send_photo(chat_id=config.ADMIN_ID,
                         photo=photo_user,
                         caption=f'Пользователь {message.from_user.first_name} | {message.from_user.id}\n',reply_markup=admin_pay_accept(client_id=client_id))
    await state.reset_state()

@dp.callback_query_handler(cb_pay.filter(action='pay_yes'))
async def accpet_subs_pay_check(call:types.CallbackQuery,callback_data:dict):
    logger.info(f'Команда accpet_subs_pay для пользователя {call.message.chat.first_name}')
    await call.answer()
    client_id = callback_data.get('client_id')
    await call.message.reply('Отправал сообщение что скоро добавят в бота')
    await bot.send_message(chat_id=client_id,
                           text='✅ Платеж успешно завершен!'
                                'В ближайшее время вам одобрят функцию\n')

@dp.callback_query_handler(cb_pay.filter(action='pay_no'))
async def cancel_pay_accept(call:types.CallbackQuery,callback_data:dict):
    logger.info(f'Команда cancel_pay_accept для пользователя {call.message.chat.first_name}')
    await call.answer()
    client_id = callback_data.get('client_id')
    await call.message.answer('Оплата удалена')
    await bot.send_message(chat_id=client_id,text=f'❌ Оплата не прошла\n'
                                                    'Если произошла ошибка, свяжитесь по контактам в боте\n')



@dp.callback_query_handler(cb.filter(action='more_check'))#IsSubs_MSG(),
async def more_check_menu(call:types.CallbackQuery):
    logger.info(f'Команда more_check_menu для пользователя {call.message.chat.first_name}')
    await call.answer()
    await call.message.edit_text(
                              '<b>Введите ваши аккаунты в формате</b>\n'
                              'log:pass\n'
                              'log:pass\n\n'
                              '<b>Важно</b>\n'
                              '-Для наилучшей работы бота, закидывайте не больше 100 штук.\n'
                              '-При неправильном формате , бот может работать не стабильно.\n'
                              '-Аккаунты должны быть отправлены одним сообщением.',reply_markup=auth_menu()
                            )
    await Check.checks.set()



@dp.message_handler(state=Check.checks)#IsSubs_MSG(),
async def check_check(message:types.Message,state:FSMContext):
    logger.info(f'Команда check_check для пользователя {message.from_user.first_name}')
    with open('proxy','r') as file:
        count_proxies = len(file.readlines())
    with open(f'no_valid_{message.from_user.first_name}.txt', 'w') as file_novalid,\
            open(f'results_{message.from_user.first_name}.txt', 'w') as file:
        accounts = message.text.split('\n')
        acc_good = {}
        regions = ['latam', 'br', 'na']
        proxy = '' #'http://pwERmR:iVTCIzRG4i@31.12.93.201:3000'#pwERmR:iVTCIzRG4i@31.12.93.201:3000
        auth_base = Auth()
        # 8 аккаунтов
        account_step = 0
        account_check = 0
        proxy_stop = 0
        message_info = await message.answer(f'Кол-во аккаунтов:<b>{len(accounts)}</b>\n'
                             f'<i>Пожалуйста, не пишите и не нажимайте ничего.Дождитесь пока бот закончит сбор информации.</i>\n')
        while account_step < len(accounts):
            login = accounts[account_step].split(':')[0]
            password = accounts[account_step].split(':')[1]
            try:
                authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)#aiohttp.client_exceptions.ClientHttpProxyError
                print(authenticate)
                print(login)
            except (ClientHttpProxyError,ContentTypeError) as e:
                    print('Смена прокси')
                    proxy_get = get_proxy()[random.randrange(count_proxies)]
                    proxy = f'http://{proxy_get["username"]}:{proxy_get["password_ip"]}:{proxy_get["port"]}'
                    # authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)
                    continue
            # Если не правильный лог пасс
            if 'error' in authenticate and authenticate['error'] == 'auth_failure':
                file_novalid.writelines(f'{login} - not valid\n')
                print(f'Не валид {login}')
                account_step += 1
                await bot.edit_message_text(chat_id=message_info.chat.id, message_id=message_info.message_id,
                                            text=f'Кол-во аккаунтов проверенно:<b>{account_check + 1}</b> из <b>{len(accounts)}</b>')
                account_check += 1
            # Если лимит по запросам с одного IP
            elif 'error' in authenticate and authenticate['error'] == 'rate_limited':
                proxy_get = get_proxy()[proxy_stop]
                proxy = f'http://{proxy_get["username"]}:{proxy_get["password_ip"]}:{proxy_get["port"]}'
                # authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)
                proxy_stop += 1
            # Если все ок и прошла аунтефикация
            else:
                await bot.edit_message_text(chat_id=message_info.chat.id, message_id=message_info.message_id,
                                            text=f'Кол-во аккаунтов проверенно:<b>{account_check + 1}</b> из <b>{len(accounts)}</b>')
                acc_good[login] = password
                access_token = authenticate['data']['access_token']
                token_id = authenticate['data']['token_id']
                puuid, name, tag ,email_verif,phone_verif= await auth_base.get_userinfo(access_token)
                entitlements_token = await auth_base.get_entitlements_token(access_token)
                region = await auth_base.get_region(access_token, token_id)
                region_output = region
                if region is None:
                    file_novalid.writelines(f'{login} - not valid\n')
                    account_step+=1
                    account_check+=1
                    continue
                if region in regions:
                    region = 'na'
                items = auth_base.get_items(item='e7c63390-eda7-46e0-bb7a-a6abdacd2433',
                                            ent_token=entitlements_token,
                                            region=region,
                                            acc_token=access_token,
                                            puuid=puuid)
                result = get_skins(items=items, login=login, password=password,email=email_verif,region=region_output,
                                   phone=phone_verif)
                print(f'Валид {login}')
                file.writelines(f'{result}\n')
                account_step += 1
                account_check += 1
    file.close()
    file_novalid.close()
    try:
        await message.reply_document(document=open(fr'results_{message.from_user.first_name}.txt', 'rb'))
    except Exception as e:
        await message.reply('Валидных аккаунтов нет')
    try:
        await message.reply_document(document=open(fr'no_valid_{message.from_user.first_name}.txt','rb'))
    except Exception as e:
        await message.reply('Невалидных аккаунтов нет')
    await state.reset_state()