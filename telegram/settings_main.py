from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client, kb_settings_main, kb_settings_main_2


# ID = None

# Команда для настроек
class FSMSettings(StatesGroup):

    # Старт настроек
    ded_choice_settings = State()
    ded_comand = State()

    ded_date = State()
    ded_time = State()


# Начало выполнения команды
async def load_choice_settings(message : types.Message, state : FSMContext):
    await FSMSettings.ded_choice_settings.set()
    async with state.proxy() as data:
        # Добавление и получение в словарь data айди юзера
        data['user_id'] = message.chat.id
    await message.reply('Выберите дедлайн, который хотите настроить:', reply_markup=kb_settings_main)

    # Вывод из БД имён всех дедлайнов


# Выход из показа дедлайна
async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


# Получение имени дедлайна
async def load_name(message : types.Message, state : FSMContext):

    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД
    async with state.proxy() as data:
        # Добавление в словарь data айди юзера и имя дедлайна
        data['ded_name'] = message.text
    await FSMSettings.next()
    await message.reply('Введите команду, которую исполнить', reply_markup=kb_settings_main_2)


async def load_command(message : types.Message, state : FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД
    async with state.proxy() as data:
        # Добавление в словарь data айди юзера и имя дедлайна
        data['ded_comand'] = message.text
    await FSMSettings.next()
    await message.reply('Введите новую дату в формате ЧЧ.ММ.ГГГГ', reply_markup=kb_settings_main)


# Настройки времени
async def load_date(message : types.Message, state : FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД
    async with state.proxy() as data:
        # Добавление в словарь data айди юзера и имя дедлайна
        data['ded_date'] = message.text
    await FSMSettings.next()
    await message.reply('Введите новое время в формате ЧЧ.ММ ')


async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ded_time'] = message.text
    # Вывод полученных результатов
        await message.reply(str(data))
    await message.answer('Выходим в главную!', reply_markup=kb_client)

    await state.finish()




# Регистрация команд для передачи

def register_handler_settings_main(db : Dispatcher):
    db.register_message_handler(load_choice_settings, lambda message : 'настройки' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state= FSMSettings.ded_choice_settings)
    db.register_message_handler(load_command, state=FSMSettings.ded_comand)
    db.register_message_handler(load_date, state=FSMSettings.ded_date)
    db.register_message_handler(load_time, state=FSMSettings.ded_time)


