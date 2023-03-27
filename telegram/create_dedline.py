# Админские настройки бота
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from keybords import kb_client
from keybords import kb_create

# ID = None

# Команда для создания дедлайна
class FSMAdmin(StatesGroup):
    ded_name = State()
    ded_description = State()
    ded_date = State()
    ded_time = State()
    ded_regularity = State()
    ded_warning = State()



# Начало выполнения команды

async def cret_ded(message : types.Message):
    await FSMAdmin.ded_name.set()

    await message.reply('Какое название будет у дедлайна?', reply_markup= kb_create)


# Выход из записи дедлайна
async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()

# Получение имени дедлайна и переход на описание

async def load_name(message : types.Message, state : FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД
    async with state.proxy() as data:
        # Добавление в словарь data айди юзера и имя дедлайна
        # Проверка на то, что имени таково дедлайна нет
        data['user_id'] = message.chat.id
        data['ded_name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание дедлайна')


# Получение описания и переход на дату

async def load_description(message : types.Message, state : FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД!!!!!!!
    async with state.proxy() as data:
        # Добавление в словарь data описание дедлайна
        data['ded_description'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите дату дедлайна формата ЧЧ.ММ.ГГГГ')



# Получение даты и переход на повторы

async def load_date(message: types.Message, state: FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД, как дату!!!!!!!!
    async with state.proxy() as data:
        # Добавление в словарь data числа
        data['ded_date'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите время дедлайна в формате ЧЧ.ММ')


async def load_time(message: types.Message, state: FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД, как дату!!!!!!!!
    async with state.proxy() as data:
        # Добавление в словарь data времени
        data['ded_time'] = message.text
    await FSMAdmin.next()
    await message.reply(
        'Теперь введите как часто повторять данный дедлайн (одноразовый - введите "один", каждую ниделю - введите "часто")')



# Получение регулярности дедлайнов и завершение
async def load_regularity(message: types.Message, state: FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД!!!!!!!!
    async with state.proxy() as data:
        # Добавление в словарь data регулярности оповещений
        data['ded_regularity'] = message.text
    await FSMAdmin.next()
    await message.reply("""За сколько вас нудно предупредить о дедлайне? 
Введите в целых часах! """)



async def load_warning(message: types.Message, state: FSMContext):
    # Тут должна быть запись данных в оперативку, а после корректного завершения в БД!!!!!!!!
    async with state.proxy() as data:
        # Добавление в словарь data часов о предупреждении
        data['ded_warning'] = int(message.text)

    # До этого нужно записать все полученные данные!!! Пока тут временная функция



    # Вывод полученных результатов
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.answer('Дедлайн создан и добавлен!', reply_markup= kb_client)

    await state.finish()






# Регистрация команд для передачи

def register_handler_create_dedline(db : Dispatcher):
    db.register_message_handler(cret_ded, lambda message : 'создать' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state= FSMAdmin.ded_name)
    db.register_message_handler(load_description, state= FSMAdmin.ded_description)
    db.register_message_handler(load_date, state=FSMAdmin.ded_date )
    db.register_message_handler(load_time, state=FSMAdmin.ded_time)
    db.register_message_handler(load_regularity, state=FSMAdmin.ded_regularity)
    db.register_message_handler(load_warning, state=FSMAdmin.ded_warning)

    # db.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
