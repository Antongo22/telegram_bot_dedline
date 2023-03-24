import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os


bot = Bot(token='6143272555:AAH_gr1NMNho_top15kU9ska0iDDUdetr9U')

dp = Dispatcher(bot)

# Показать, что бот запущен
async def on_startup(_):
    print("Бот начал работать!")

# Приветственная команда бота
@dp.message_handler(commands=['start'])
async def commands_start(message : types.message):
    await bot.send_message(message.from_user.id, """Здравствуйте! Вас приветсвует Дедлайн бот! 
С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""")


# Команды, высылающая пользователю функции бота
@dp.message_handler(commands=['help'])
async def commands_start(message : types.message):
    await bot.send_message(message.from_user.id, """С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""")

# На команду высылает наш сайт
@dp.message_handler(commands=['Сайт'])
async def site(message : types.message):
    await bot.send_message(message.from_user.id, """www.2Develop.site""")



# Тест по говнокоду)
@dp.message_handler()
async def ask_govnokod(message : types.Message):
    if message.text == "Кто пишет говнокод?":
        await bot.send_message(message.from_user.id,"Кто спрашивает тот и пишет")
        await bot.send_message(message.from_user.id, "И вообще, выключи компьютер!")

    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю!")


# парабетры цикличности бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)