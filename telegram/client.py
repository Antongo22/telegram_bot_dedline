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


# Команда, для создания дедлайна
async def create_ded_line(message: types.message):
    await message.answer("""Как назовём дедлайн?""")

# Команда по выводу на экран дедлайнов
async def show_ded_lines(message: types.message):
    await message.answer("""Вот ваши дедлайны:
Какой показать?""")

# Комманда для настроекти
async def ded_line_settings(message: types.message):
    await message.answer("""Что будем настраивать?""")


# Передача команд клиента
def register_handlers_client(dp: Dispatcher):
    # Бинд команд на кнопки
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(commands_help, commands=['help'])
    dp.register_message_handler(site, commands=['сайт'])
    dp.register_message_handler(create_ded_line, commands=['создать'])
    dp.register_message_handler(show_ded_lines, commands=['показать'])
    dp.register_message_handler(ded_line_settings, commands=['настройки'])
