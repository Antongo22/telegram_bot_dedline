# Соединение всех файлов
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='')  # Объявление и создание бота
dp = Dispatcher(bot, storage=storage)
