from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client, kb_show


# ID = None

# Команда для настроек
class FSMReminderDel(StatesGroup):
    ded_ok = State()
    ded_del_d = State()



# Начало выполнения команды
async def start_data_time(message : types.Message, state : FSMContext):
    await FSMReminderDel.ded_ok.set()
    async with state.proxy() as data:
        # Добавление и получение в словарь data айди юзера
        data['user_id'] = message.chat.id
    await message.reply('Введите номер дедлайна, который вы хотите удалить', reply_markup=kb_show)



# Выход из показа дедлайна
async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


async def load_ok(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['ded_name'] = message.text
    await FSMReminderDel.next()
    await message.reply('Вы точно хотите удалить этот дедлайн? Да/Нет')


#Считываем настройки
async def load_del_d(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['ded_del'] = message.text

        if data['ded_del'] == 'Да':
            await message.answer('Дедлайн удалён!')
            await message.answer('Выходим в главную!', reply_markup=kb_client)

        else:
            await message.answer('Отменено!')
            await message.answer('Выходим в главную!', reply_markup=kb_client)

        await message.reply(str(data))


    await state.finish()



# Регистрация команд для передачи
def register_handler_settings_del(db : Dispatcher):
    db.register_message_handler(start_data_time, lambda message : 'удалить дедлайн' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_ok, state=FSMReminderDel.ded_ok)
    db.register_message_handler(load_del_d, state=FSMReminderDel.ded_del_d)

