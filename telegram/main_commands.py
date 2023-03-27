from aiogram import types, Dispatcher
from create_bot import dp, bot
from keybords import kb_client


# Приветственная команда бота
async def commands_start(message: types.message):
    await message.answer("""Здравствуйте! Вас приветсвует Дедлайн бот! 
С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""", reply_markup=kb_client)


# Команды, высылающая пользователю функции бота

async def commands_help(message: types.message):
    await message.answer("""С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""")


# На команду высылает наш сайт
async def site(message: types.message):
    await message.answer("""www.2Develop.site""")


# Передача команд клиента
def register_handlers_client(dp: Dispatcher):
    # Бинд команд на кнопки
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(site, lambda message : 'сайт' in message.text)

