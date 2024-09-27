from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('btn','action')

def auth_menu_eng(menu=None):
    if menu == 'Auth':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.row(InlineKeyboardButton(text='🌟 Skin Collection', callback_data=cb.new(action='skins_eng')),
                     InlineKeyboardButton(text='🛍️ Store', callback_data=cb.new(action='store_eng')),
                     InlineKeyboardButton(text='🤖 Agents', callback_data=cb.new(action='agent_eng')))
        #keyboard.add(InlineKeyboardButton(text='🌌 Night Market', callback_data=cb.new(action='night_market_eng')))

        keyboard.add(InlineKeyboardButton(text='ℹAccount Information', callback_data=cb.new(action='account_eng')),
                     InlineKeyboardButton(text='🚪 Log Out', callback_data=cb.new(action='exit_eng')))
    elif menu == 'Login':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🔑 Log In', callback_data=cb.new(action='login_eng')),
                     InlineKeyboardButton(text='👨‍💻 Support', callback_data=cb.new(action='support_eng')))
        keyboard.add(InlineKeyboardButton(text='⚙Settings', callback_data=cb.new(action='settings_eng')))
    elif menu == 'Cancel':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🚫 Cancel', callback_data=cb.new(action='cancel_eng')))

    else:
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🔙 Back', callback_data=cb.new(action='back_eng')))
    return keyboard
