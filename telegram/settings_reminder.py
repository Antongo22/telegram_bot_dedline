from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client, kb_show
from datetime import datetime


class FSMReminder(StatesGroup):  # Команда для настроек - ещё одно время оповещения
    ded_name = State()
    ded_date = State()
    ded_time = State()


async def start_data_time(message: types.Message, state: FSMContext):  # Начало выполнения команды
    await FSMReminder.ded_name.set()
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


async def load_name(message: types.Message, state: FSMContext):  # Получение имени дедлайна
    async with state.proxy() as data:
        data['ded_name'] = message.text
    await FSMReminder.next()
    await message.reply('Введите новую дату оповещения в формате ЧЧ.ММ.ГГГГ')


async def load_date(message: types.Message, state: FSMContext):  # Получаем дату нового оповещения
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
                int(d_date[1]) > month and int(d_date[2]) >= year) or (int(d_date[2]) > year):

            try:
                datetime.strptime(message.text, '%d.%m.%Y')
                async with state.proxy() as data:
                    data['ded_date'] = message.text
                await FSMReminder.next()
                await message.reply('Введите новое время оповещения в формате ЧЧ.ММ')

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


async def load_time(message: types.Message, state: FSMContext):  # Получаем время нового оповещения
    from datetime import datetime

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
        d_time = message.text.split('.')
        try:
            import datetime
            time_obj = datetime.datetime.strptime(message.text, '%H.%M').time()
            assert time_obj.hour < 24 and time_obj.minute < 60

            async with state.proxy() as data:
                data['ded_time'] = message.text
                await message.reply(str(data))
            await message.answer('Время оповещения добавлено!')
            await message.answer('Выходим в главную!', reply_markup=kb_client)

            await state.finish()

        except (ValueError, AssertionError):

            await message.reply('Вы ввели неправильный формат даты или эта дата недоступна!')
            await message.answer("Превышено допустимое количество попыток! Попробуйте создать дедлайн ещё раз!",
                                 reply_markup=kb_client)
            await state.finish()

    except:
        await message.reply('Вы ввели неправильный формат даты или эта дата недоступна!')

        await message.answer("Превышено допустимое количество попыток! Попробуйте создать дедлайн ещё раз!",
                             reply_markup=kb_client)
        await state.finish()



def register_handler_settings_reminder(db: Dispatcher):  # Регистрация команд для передачи
    db.register_message_handler(start_data_time, lambda message: 'добавить точку оповещения' in message.text,
                                state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_name, state=FSMReminder.ded_name)
    db.register_message_handler(load_date, state=FSMReminder.ded_date)
    db.register_message_handler(load_time, state=FSMReminder.ded_time)
