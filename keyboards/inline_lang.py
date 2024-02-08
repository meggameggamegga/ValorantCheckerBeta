from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb_settings = CallbackData('btn','action')

def set_language_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🇷🇺Ru',callback_data=cb_settings.new(action='ru')))
    keyboard.add(InlineKeyboardButton(text='🇺🇸En',callback_data=cb_settings.new(action='en')))
    return keyboard