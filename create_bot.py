# Соединение всех файлов
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# Объявление и создание бота
bot = Bot(token='6143272555:AAH_gr1NMNho_top15kU9ska0iDDUdetr9U')
dp = Dispatcher(bot, storage=storage)
