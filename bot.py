from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):  # Показать, что бот запущен
    print("Бот начал работать!")


from telegram import main_commands, create_dedline, show_dedline, other, settings_time, settings_name, \
    settings_reminder, \
    settings_reminder_del, settings_del

# Вызов базы команд
main_commands.register_handlers_client(dp)

create_dedline.register_handler_create_dedline(dp)

show_dedline.register_handler_show_dedline(dp)

settings_time.register_handler_settings_time(dp)

settings_name.register_handler_settings_neme(dp)

settings_reminder.register_handler_settings_reminder(dp)

settings_reminder_del.register_handler_settings_reminder_del(dp)

settings_del.register_handler_settings_del(dp)

other.register_handlers_other(dp)  # Вызов остальных команд (всегда ниже остальных)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # параметры цикличности бота
