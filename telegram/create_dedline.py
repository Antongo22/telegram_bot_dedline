from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client
from keybords import kb_create
from datetime import datetime


class FSMCreate(StatesGroup):  # Команда для создания дедлайна
    ded_name = State()
    ded_description = State()
    ded_date = State()
    ded_time = State()
    ded_regularity = State()
    ded_warning_date = State()
    ded_warning_time = State()


async def cret_ded(message: types.Message):  # Начало выполнения команды
    await FSMCreate.ded_name.set()
    await message.reply('Какое название будет у дедлайна?', reply_markup=kb_create)


async def cancel_handler(message: types.Message, state: FSMContext):  # Выход из записи дедлайна
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


async def load_name(message: types.Message, state: FSMContext):  # Получение имени дедлайна и переход на описание
    async with state.proxy() as data:
        data['user_id'] = message.chat.id
        data['ded_name'] = message.text
    await FSMCreate.next()
    await message.reply('Введите описание дедлайна')


async def load_description(message: types.Message, state: FSMContext):  # Получение описания и переход на дату
    async with state.proxy() as data:
        data['ded_description'] = message.text
    await FSMCreate.next()
    await message.reply('Введите дату дедлайна формата ЧЧ.ММ.ГГГГ')


async def load_date(message: types.Message, state: FSMContext):  # Получение даты дедлайна
    # Получение конкретной даты и времени
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    hour = current_date.hour
    minute = current_date.minute
    date = f"{year}.{month}.{day}"
    time = f"{hour}.{minute}"

    try:  # Проверка на доступность даты
        d_date = message.text.split('.')
        if (int(d_date[0]) >= day and int(d_date[1]) >= month and int(d_date[2]) >= year) or (
                int(d_date[1]) >= month and int(d_date[2]) >= year) or (int(d_date[2]) > year):

            try:
                datetime.strptime(date, '%d.%m.%Y')
                async with state.proxy() as data:
                    data['ded_date'] = message.text
                    print("продолжим")
                await FSMCreate.next()
                await message.reply('Введите время дедлайна в формате ЧЧ.ММ')

            except ValueError:
                await message.reply('Вы ввели неправильный формат даты или эта дата недоступна!')
                await message.answer("Превышено допустимое количество попыток! Попробуйте создать дедлайн ещё раз!",
                                     reply_markup=kb_client)
                await state.finish()


        else:
            await message.reply('Вы ввели неправильный формат даты или эта дата недоступна!')
            await message.answer("Превышено допустимое количество попыток! Попробуйте создать дедлайн ещё раз!",
                                 reply_markup=kb_client)
            await state.finish()

    except:
        await message.reply('Вы ввели неправильный формат даты или эта дата недоступна!')

        await message.answer("Превышено допустимое количество попыток! Попробуйте создать дедлайн ещё раз!",
                             reply_markup=kb_client)
        await state.finish()


async def load_time(message: types.Message, state: FSMContext):  # Получение времени дедлайна
    async with state.proxy() as data:
        data['ded_time'] = message.text
    await FSMCreate.next()
    await message.reply(
        'Теперь введите как часто повторять данный дедлайн (одноразовый - введите "один", каждую ниделю - введите "часто")')


async def load_regularity(message: types.Message, state: FSMContext):  # Получение регулярности дедлайнов и завершение
    async with state.proxy() as data:
        data['ded_regularity'] = message.text.lower()
    await FSMCreate.next()
    await message.reply(
        """Введите дату, когда вас предупредить о дедлайне формата ЧЧ.ММ.ГГГГ. В настройках вы сможете добавить ещё одну точку""")


async def load_warning_date(message: types.Message, state: FSMContext):  # Получение даты предупреждения
    async with state.proxy() as data:
        data['ded_warning_date'] = message.text
        await FSMCreate.next()
        await message.reply(
            """Введите время, когда вас предупредить о дедлайне формата ЧЧ.ММ. В настройках вы сможете добавить ещё одну точку""")


async def load_regularity_time(message: types.Message, state: FSMContext):  # Получение времени предупреждения
    async with state.proxy() as data:
        data['ded_warning_time'] = message.text

    # Вывод полученных результатов
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.answer('Дедлайн создан и добавлен!')
    await message.answer('Выходим в главную!', reply_markup=kb_client)
    await state.finish()


def register_handler_create_dedline(db: Dispatcher):  # Регистрация команд для передачи
    db.register_message_handler(cret_ded, lambda message: 'создать' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state=FSMCreate.ded_name)
    db.register_message_handler(load_description, state=FSMCreate.ded_description)
    db.register_message_handler(load_date, state=FSMCreate.ded_date)
    db.register_message_handler(load_time, state=FSMCreate.ded_time)
    db.register_message_handler(load_regularity, state=FSMCreate.ded_regularity)
    db.register_message_handler(load_warning_date, state=FSMCreate.ded_warning_date)
    db.register_message_handler(load_regularity_time, state=FSMCreate.ded_warning_time)
