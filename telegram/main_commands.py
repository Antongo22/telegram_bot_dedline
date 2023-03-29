from aiogram import types, Dispatcher
from create_bot import dp, bot
from keybords import kb_client, kb_settings_main


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


async def settings(message: types.message):
    await message.answer("""Что вы хотите сделать?""", reply_markup = kb_settings_main )

async def cancellation(message: types.message):
    await message.reply("""Ок""", reply_markup=kb_client )

# Передача команд клиента
def register_handlers_client(dp: Dispatcher):
    # Бинд команд на кнопки
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(site, lambda message : 'сайт разработчиков' in message.text)
    dp.register_message_handler(settings, lambda message: 'настройки' in message.text)
    dp.register_message_handler(cancellation, lambda message: 'отмена' in message.text)


