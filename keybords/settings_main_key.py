from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок
but_cancellation = KeyboardButton('отмена')

# Объект клавиатуры
kb_settings_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Добавление на клавиатуру кнопок. insert делает так, чтобыв ззаполнялось по размерам надписей, тоесть красиво
kb_settings_main.insert(but_cancellation)


