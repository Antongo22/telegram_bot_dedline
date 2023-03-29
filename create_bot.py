# Соединение всех файлов
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='6143272555:AAH_gr1NMNho_top15kU9ska0iDDUdetr9U')  # Объявление и создание бота
dp = Dispatcher(bot, storage=storage)
