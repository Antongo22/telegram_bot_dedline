from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок
but_cancellation = KeyboardButton('отмена')

but_change = KeyboardButton('настроить время')
but_name = KeyboardButton('настроить имя/описание')
but_reminder = KeyboardButton('добавить точку оповещения')
but_reminder_del = KeyboardButton('удалить точку оповещения')
but_del = KeyboardButton('удалить дедлайн')
# Объект клавиатуры
kb_settings_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Добавление на клавиатуру кнопок. insert делает так, чтобыв заполнялось по размерам надписей, тоесть красиво
kb_settings_main.insert(but_change).insert(but_name).insert(but_reminder).insert(but_reminder_del).insert(but_del).insert(but_cancellation)