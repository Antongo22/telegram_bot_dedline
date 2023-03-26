from aiogram.utils import executor
from create_bot import dp

# Показать, что бот запущен
async def on_startup(_):
    print("Бот начал работать!")

from telegram import main_commands, create_dedline, other

# Вызов клиентсокй базы команд
main_commands.register_handlers_client(dp)

create_dedline.register_handler_admin(dp)

# Вызов остальных команд (всегда ниже остальных)
other.register_handlers_other(dp)



# парабетры цикличности бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)