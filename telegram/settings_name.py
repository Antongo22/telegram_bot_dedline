from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client, kb_show


class FSMSetName(StatesGroup):  # Команда для настроек - новое имя и описание
    ded_name = State()
    ded_new_name = State()
    ded_new_new_description = State()


async def start_data_time(message: types.Message, state: FSMContext):  # Начало выполнения команды
    await FSMSetName.ded_name.set()
    async with state.proxy() as data:
        # Добавление и получение в словарь data айди юзера
        data['user_id'] = message.chat.id
    await message.reply('Введите номер дедлайна, который вы хотите настроить', reply_markup=kb_show)


async def cancel_handler(message: types.Message, state: FSMContext):  # Выход из показа дедлайна
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


async def load_name(message: types.Message, state: FSMContext):  # Получение имени дедлайна для настроек
    async with state.proxy() as data:
        data['ded_name'] = message.text
    await FSMSetName.next()
    await message.reply('Введите новое имя дедлайна!')


async def new_name(message: types.Message, state: FSMContext):  # Получение нового имени дедлайна
    async with state.proxy() as data:
        data['ded_new_name'] = message.text
    await FSMSetName.next()
    await message.reply('Введите новое описание дедлайна')


async def new_description(message: types.Message, state: FSMContext):  # Получение нового описания дедлайна
    async with state.proxy() as data:
        data['ded_new_new_description'] = message.text
        await message.reply(str(data))
    await message.answer('Дедлайн переименован!')
    await message.answer('Выходим в главную!', reply_markup=kb_client)

    await state.finish()


def register_handler_settings_neme(db: Dispatcher):  # Регистрация команд для передачи
    db.register_message_handler(start_data_time, lambda message: 'настроить имя/описание' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state=FSMSetName.ded_name)
    db.register_message_handler(new_name, state=FSMSetName.ded_new_name)
    db.register_message_handler(new_description, state=FSMSetName.ded_new_new_description)