from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок
but_one = KeyboardButton('один')
but_reg = KeyboardButton('часто')
but_cancellation = KeyboardButton('отмена')

# Объект клавиатуры
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Добавление на клавиатуру кнопок. insert делает так, чтобыв ззаполнялось по размерам надписей, тоесть красиво
kb_reg.insert(but_one).insert(but_reg).insert(but_cancellation)
