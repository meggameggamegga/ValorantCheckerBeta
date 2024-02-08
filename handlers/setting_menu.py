
import logging
from filter.Language_filter import IsLanguageENG_CALL
from filter.is_admin import *

from keyboards.inline import cb
from keyboards.inline_lang import cb_settings, set_language_menu

from main import dp

db = DataBase('test.db')


from aiogram import types


logger = logging.getLogger('app.base.setting_menu')

@dp.callback_query_handler(IsLanguageENG_CALL(),cb.filter(action='settings_eng'))
async def settings_change(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('🌎 Select a language',reply_markup=set_language_menu())

@dp.callback_query_handler(cb.filter(action='settings'))
async def settings_change(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('🌎Выберите язык:',reply_markup=set_language_menu())

@dp.callback_query_handler(cb_settings.filter(action='ru'))
async def change_lang_ru(call:types.CallbackQuery):
    db.set_language(call.message.chat.id,'RU')
    await call.message.delete()
    await call.message.answer('🇷🇺Язык изменен на <b>RU</b>')

@dp.callback_query_handler(cb_settings.filter(action='en'))
async def change_lang_eu(call:types.CallbackQuery):
    db.set_language(call.message.chat.id,'EU')
    await call.message.delete()
    await call.message.answer('🇺🇸Language changed to <b>EN</b>')
