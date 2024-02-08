from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('btn','action')
cb_pay = CallbackData('btn','action','client_id')
def auth_menu(menu=None):
    if menu =='Auth':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.row(InlineKeyboardButton(text='🌟 Коллекция скинов',callback_data=cb.new(action='skins')),
                     InlineKeyboardButton(text='🛍️ Магазин',callback_data=cb.new(action='store')),
                     InlineKeyboardButton(text='🤖Агенты',callback_data=cb.new(action='agent')))
        #keyboard.add(InlineKeyboardButton(text='🛒 Продать аккаунт', callback_data=cb.new(action='sell_acc')))

        keyboard.add(InlineKeyboardButton(text='🌌Ночной маркет',callback_data=cb.new(action='night_market')))

        keyboard.add(InlineKeyboardButton(text='ℹИнформация по аккаунту',callback_data=cb.new(action='account')),
                    InlineKeyboardButton(text='🚪 Выход',callback_data=cb.new(action='exit')))
    elif menu =='Login':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🔑 Войти',callback_data=cb.new(action='login')),
                     InlineKeyboardButton(text='👨‍💻 Поддержка',callback_data=cb.new(action='support')))
                     #InlineKeyboardButton(text='💎Массовый чек', callback_data=cb.new(action='more_check')))
        keyboard.add(InlineKeyboardButton(text='⚙Настройки',callback_data=cb.new(action='settings')))
        #keyboard.add(InlineKeyboardButton(text='Оплатить подписку 💳',callback_data=cb.new(action='pay_check')))
    elif menu =='Cancel':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🚫 Отмена',callback_data=cb.new(action='cancel')))
    elif menu == 'Admin':
        keyboard = InlineKeyboardMarkup(inline_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Посмотреть кол-во пользователей', callback_data=cb.new(action='check_users')),
                     InlineKeyboardButton(text='Сделать рассылку',callback_data=cb.new(action='send_messages')))
        keyboard.add(InlineKeyboardButton(text='Добавить селлера',callback_data=cb.new(action='add_seller')),
                     InlineKeyboardButton(text='Удалить селлера',callback_data=cb.new(action='delete_seller')))
        keyboard.add(InlineKeyboardButton(text='Добавить в массовый чек',callback_data=cb.new(action='add_to_check')),
                     InlineKeyboardButton(text='Добавить в пробный чек',callback_data=cb.new(action='add_test_check')))
    elif menu =='messages':
        keyboard = InlineKeyboardMarkup(inline_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Да', callback_data=cb.new(action='yes')),
                     InlineKeyboardButton(text='Нет',callback_data=cb.new(action='no')))

    else:
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='🔙 Назад',callback_data=cb.new(action='back')))
    return keyboard

def pay_check():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Выслать чек',callback_data=cb.new(action='send_pay')),
                 InlineKeyboardButton(text='Отмена',callback_data=cb.new(action='cancel_pay')))
    return keyboard

def admin_pay_accept(client_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Платеж пришел',callback_data=cb_pay.new(action='pay_yes',
                                                                                    client_id=client_id)),
                 InlineKeyboardButton(text='Не пришел',callback_data=cb_pay.new(action='pay_no',
                                                                                client_id=client_id)))
    return keyboard
