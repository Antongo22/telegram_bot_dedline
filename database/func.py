from datetime import datetime, timedelta

from database.database import cursor, conn
from aiogram import types
import asyncio

loop = asyncio.get_event_loop()

# функция для добавления нового дедлайна
async def add_deadline(data):
    # получаем параметры дедлайна
    user_id = data['user_id']
    title = data['ded_name']
    description = data['ded_description']
    date = data['ded_date'].replace('.', '-')
    time = data['ded_time']
    war_date = data['ded_warning_date'].replace('.', '-')
    war_time = data['ded_warning_time']

    print('saa')

    # добавляем дедлайн в базу данных
    cursor.execute("""
    INSERT INTO deadlines (user_id, title, description, date, time, ded_warning_date, ded_warning_time)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, date, time, war_date, war_time))
    conn.commit()

    # отправка сообщения
    await check_deadlines(...)

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
        _, user_id, title, description, date, time, war_date, war_time = deadline
        text += f'{title}\n{description}\nДата: {date}\nВремя: {time}\nКогда предупредить: {war_date} {war_time} \n\n'

    # отправка сообщения
    await check_deadlines(...)

# функция для отправки напоминания о дедлайнах
async def check_deadlines(message : types.Message):
    from telegram.create_dedline import ded_send_ded, ded_send_warning

    # получаем текущую дату и время
    now = datetime.now()

    print("aaa")

    # получаем все дедлайны, у которых дата и время больше или равны текущим
    cursor.execute("""
    SELECT * FROM deadlines
    WHERE date >= ? AND time >= ?
    """, (now.strftime('%d-%m-%Y'), now.strftime('%H.%M')))
    deadlines = cursor.fetchall()

    print(deadlines)

    # отправляем напоминания о дедлайнах
    for deadline in deadlines:
        _, user_id, title, description, dates, time, war_date, war_time = deadline

        print(dates.split(';'))

        for date in dates.split(';'):
            print("2")
            deadline_datetime_1 = datetime.strptime(f'{date} {time}', '%d-%m-%Y %H.%M')
            print("3")
            deadline_datetime_2 = datetime.strptime(f'{war_date} {war_time}', '%d-%m-%Y %H.%M')
            print("4")
            delta_1 = deadline_datetime_1 - datetime.now()
            print("5")
            delta_2 = deadline_datetime_2 - datetime.now()

            print(delta_1.total_seconds())
            print(delta_2.total_seconds())
            
            if (delta_1.total_seconds() <= 10 and delta_1.total_seconds() >= -10):
                # получаем пользователей, которым нужно отправить напоминание
                cursor.execute("""
                SELECT user_id FROM deadlines
                WHERE id = ?
                """, (deadline[0],))
                print("delta_1")

                # отправка оповещения
                await ded_send_ded(_, title, description, war_date, war_time, user_id)
            elif (delta_2.total_seconds() <= 10 and delta_2.total_seconds() >= -10):
                # получаем пользователей, которым нужно отправить напоминание
                cursor.execute("""
                SELECT user_id FROM deadlines
                WHERE id = ?
                """, (deadline[0],))
                print("delta_2")

                # отправка оповещения
                await ded_send_warning(_, title, description, war_date, war_time, user_id)

    print("ожидание")
    # ждём 1 минуту и запускаем функцию снова
    await asyncio.sleep(60 - datetime.now().second)
    await check_deadlines(...)


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

