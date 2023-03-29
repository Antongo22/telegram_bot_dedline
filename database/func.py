from datetime import datetime, timedelta

from database.database import cursor, conn

import asyncio

loop = asyncio.get_event_loop()

# функция для добавления нового дедлайна
async def add_deadline(data):
    # получаем параметры дедлайна
    user_id = data['user_id']
    title = data['ded_name']
    description = data['ded_description']
    date = data['ded_date']
    time = data['ded_time']
    reminder = data['ded_warning']

    # проверяем, что дата и время указаны в правильном формате
    try:
        datetime.strptime(date, '%d-%m-%Y')
        datetime.strptime(time, '%H:%M')
    except ValueError:
        return

    # добавляем дедлайн в базу данных
    cursor.execute("""
    INSERT INTO deadlines (user_id, title, description, date, time, reminder)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, date, time, reminder))
    conn.commit()

# функция для получения списка всех дедлайнов
async def list_deadlines(data):
    # получаем все дедлайны из базы данных
    cursor.execute("""
    SELECT * FROM deadlines
    """)
    deadlines = cursor.fetchall()

    # проверяем, что есть хотя бы один дедлайн
    if not deadlines:
        return

    # формируем текст сообщения со списком дедлайнов
    text = '<b>Ваши дедлайны:</b>\n\n'
    for deadline in deadlines:
        _, user_id, title, description, date, time, reminder = deadline
        text += f'{title}\n{description}\nДата: {date}\nВремя: {time}\nЗа сколько предупредить: {reminder} мин.\n\n'

    # отправка сообщения

# функция для отправки напоминания о дедлайнах
async def check_deadlines():
    # получаем текущую дату и время
    now = datetime.now()

    # получаем все дедлайны, у которых дата и время больше или равны текущим
    cursor.execute("""
    SELECT * FROM deadlines
    WHERE date >= ? AND time >= ?
    """, (now.strftime('%Y-%m-%d'), now.strftime('%H:%M')))
    deadlines = cursor.fetchall()

    # отправляем напоминания о дедлайнах
    for deadline in deadlines:
        _, user_id, title, description, dates, time, reminder = deadline

        for date in dates.split(';'):
            deadline_datetime = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
            delta = deadline_datetime - now
            if (delta <= timedelta(minutes=reminder) and delta >= timedelta(minutes=reminder-1)):
                # получаем пользователей, которым нужно отправить напоминание
                cursor.execute("""
                SELECT user_id FROM deadlines
                WHERE id = ?
                """, (deadline[0],))

                # отправка оповещения
                # await bot.send_message(user_id, f'<b>{title}</b>\n<b>{description}</b>\nОкончание делайна через: {round(delta.total_seconds() / 60)} мин.\n', parse_mode=ParseMode.HTML)
            elif (-10 <= delta.total_seconds() and 10 >= delta.total_seconds()):
                # получаем пользователей, которым нужно отправить напоминание
                cursor.execute("""
                            SELECT user_id FROM deadlines
                            WHERE id = ?
                            """, (deadline[0],))

            # отправка оповещения
            # await bot.send_message(user_id, f'<b>{"Дедлайн"}</b>\n<b>{title}</b>\n<b>{description}</b>\n!Дедлайн!\n', parse_mode=ParseMode.HTML)

    # ждём 1 минуту и запускаем функцию снова
    await asyncio.sleep(30)
    while True:
        now = datetime.now()
        if now.second == 0:
            break
        await asyncio.sleep(1)
    loop.create_task(check_deadlines())


def update_time(data):
    # получаем параметры дедлайна
    user_id = data['user_id']
    date = data['ded_date']
    time = data['ded_time']

    # проверяем, что дата и время указаны в правильном формате
    try:
        datetime.strptime(date, '%d-%m-%Y')
        datetime.strptime(time, '%H:%M')
    except ValueError:
        return

    # добавляем дедлайн в базу данных
    cursor.execute("""
        UPDATE deadlines SET date=?, time=? WHERE user_id = ?
        """, (date, time, user_id))
    conn.commit()

def add_new_time(data):
    # получаем параметры дедлайна
    user_id = data['user_id']
    date = data['ded_date']
    time = data['ded_time']

    # проверяем, что дата и время указаны в правильном формате
    try:
        datetime.strptime(date, '%d-%m-%Y')
        datetime.strptime(time, '%H:%M')
    except ValueError:
        return

    # добавляем дедлайн в базу данных
    cursor.execute("""
        UPDATE deadlines SET date=date || ';' || ?, time=time || ';' || ? WHERE user_id = ?
        """, (date, time, user_id))
    conn.commit()

# # обработчик команды "/start"
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.reply('Привет! Я бот для создания дедлайнов. Для списка команд используйте /help.')
#
# # обработчик команды "/help"
# @dp.message_handler(commands=['help'])
# async def help(message: types.Message):
#     text = '''
#     Доступные команды:
#
#     /add <название> <описание> <дата> <время> <за сколько предупредить> - добавить новый дедлайн
#     /list - список всех дедлайнов
#     /help - помощь
#     '''
#     await message.reply(text, parse_mode=ParseMode.MARKDOWN)

# # обработчик команды "/add"
# @dp.message_handler(commands=['add'])
# async def add(message: types.Message):
#     await add_deadline(message)
#
# # обработчик команды "/list"
# @dp.message_handler(commands=['list'])
# async def list(message: types.Message):
#     await list_deadlines(message)
