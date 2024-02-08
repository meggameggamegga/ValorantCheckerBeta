from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb_seller_lk = CallbackData('btn','action')


def seller_lk():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Установить статус сделки',callback_data=cb_seller_lk.new(action='set_lk')))
    keyboard.add(InlineKeyboardButton(text='Вывести сделки',callback_data=cb_seller_lk.new(action='get_deals')))
    return keyboard