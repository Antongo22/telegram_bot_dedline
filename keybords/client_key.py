from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок
but_commands_help = KeyboardButton('/help')
but_site = KeyboardButton('/сайт')
but_create_ded_line = KeyboardButton('/создать')
but_show_ded_lines = KeyboardButton('/показать')
but_ded_line_settings = KeyboardButton('/настройки')

# Объект клавиатуры
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Добавление на клавиатуру кнопок. insert делает так, чтобыв ззаполнялось по размерам надписей, тоесть красиво
kb_client.insert(but_commands_help).insert(but_site).insert(but_create_ded_line).insert(but_show_ded_lines).insert(but_ded_line_settings)