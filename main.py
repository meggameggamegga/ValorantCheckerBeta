import logging

from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

import config
from src.middlewate import ChannelMiddleware

bot = Bot(config.BOT_TOKEN,parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
#release-07.06-shipping-4-983570

def init_logger(name): #Имя логгера
    logger = logging.getLogger(name)#Устанавливаем логгер с нужны именем(главный логгер)
    FORMAT = logging.Formatter('%(asctime)s-%(name)s:%(lineno)s-%(levelname)s-%(message)s')#Создаем формат вывода сообщений
    logger.setLevel(logging.DEBUG)#Устанавливаем левел информацию для логгера
    sh = logging.StreamHandler()#Обработчик для записи в консоль
    sh.setFormatter(FORMAT)#Устанавливаем на хендлер формат вывода инфы
    fh = logging.FileHandler(filename='logs.log',encoding='UTF8')#Устанавливаем хенде
    fh.setFormatter(FORMAT)#
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('Логгер успешно установлен')



logger = logging.getLogger('app.main')





async def on_startup(_):
    await bot.send_message(config.ADMIN_ID,'Бот запустился')
    logger.info('Бот запущен')





if __name__ == '__main__':
    from handlers import dp
    #dp.middleware.setup(ChannelMiddleware(bot))
    init_logger('app')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)