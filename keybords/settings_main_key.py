from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок
but_cancellation = KeyboardButton('отмена')

but_change = KeyboardButton('настроить время')
but_name = KeyboardButton('настроить имя/описание')
# Объект клавиатуры
kb_settings_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Добавление на клавиатуру кнопок. insert делает так, чтобыв заполнялось по размерам надписей, тоесть красиво
kb_settings_main.insert(but_cancellation).insert(but_change).insert(but_name)