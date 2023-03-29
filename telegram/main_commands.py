from aiogram import types, Dispatcher
from create_bot import dp, bot
from keybords import kb_client, kb_settings_main


async def commands_start(message: types.message):  # Приветственная команда бота
    await message.answer("""Здравствуйте! Вас приветсвует Дедлайн бот! 
С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""", reply_markup=kb_client)


async def commands_help(message: types.message):  # Команды, высылающая пользователю функции бота
    await message.answer("""С моей помощью вы можете запланировать события, о которых я буду Вас предупреждать!""")


async def site(message: types.message):  # На команду высылает наш сайт
    await message.answer("""www.2Develop.site""")


async def settings(message: types.message):  # Команда настроек
    await message.answer("""Что вы хотите сделать?""", reply_markup=kb_settings_main)


async def cancellation(message: types.message):  # Команда отмены, при настройках
    await message.reply("""Ок""", reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):  # Передача команд клиента
    # Бинд команд на кнопки
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(site, lambda message: 'сайт разработчиков' in message.text)
    dp.register_message_handler(settings, lambda message: 'настройки' in message.text)
    dp.register_message_handler(cancellation, lambda message: 'отмена' in message.text)