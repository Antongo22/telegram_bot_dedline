from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client, kb_show


# ID = None

# Команда для настроек
class FSMSetData(StatesGroup):
    ded_name = State()
    ded_date = State()
    ded_time = State()


# Начало выполнения команды
async def start_data_time(message : types.Message, state : FSMContext):
    await FSMSetData.ded_name.set()
    async with state.proxy() as data:
        # Добавление и получение в словарь data айди юзера
        data['user_id'] = message.chat.id
    await message.reply('Введите название дедлайна, который вы хотите настроить', reply_markup=kb_show)



# Выход из показа дедлайна
async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


async def load_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['ded_name'] = message.text
    await FSMSetData.next()
    await message.reply('Введите новую дату в формате ЧЧ.ММ.ГГГГ')

#Считываем настройки
async def load_date(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['ded_date'] = message.text
    await FSMSetData.next()
    await message.reply('Введите новое время в формате ЧЧ.ММ')


async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ded_time'] = message.text
        await message.reply(str(data))
    await message.answer('Данные обновлены!')
    await message.answer('Выходим в главную!', reply_markup=kb_client)

    await state.finish()



# Регистрация команд для передачи

def register_handler_settings_time(db : Dispatcher):
    db.register_message_handler(start_data_time, lambda message : 'настроить время' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state=FSMSetData.ded_name)
    db.register_message_handler(load_date, state=FSMSetData.ded_date)
    db.register_message_handler(load_time, state=FSMSetData.ded_time)


