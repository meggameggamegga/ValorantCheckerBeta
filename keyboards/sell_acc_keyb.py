from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb_sell_acc = CallbackData('btn','action')
cb_sell_buyer = CallbackData('btn','action','client_id','label')

def sell_acc_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Отправить',callback_data=cb_sell_acc.new(action='send_acc')))
    keyboard.add(InlineKeyboardButton(text='Назад',callback_data=cb_sell_acc.new(action='cancel_acc')))
    return keyboard

def sell_acc_buyer(user_id,label):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Отправить цену',callback_data=cb_sell_buyer.new(action='send_price',
                                                                                            client_id=user_id,
                                                                                            label = label)))
    keyboard.add(InlineKeyboardButton(text='Отказаться', callback_data=cb_sell_buyer.new(action='cancel_price',
                                                                                             client_id=user_id,
                                                                                             label = label)))
    return keyboard

def sell_acc_client(link):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Перейти к сделке',url=f'https://t.me/{link}'))#Тут тг чела
    return keyboard