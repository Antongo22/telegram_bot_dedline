from aiogram import types, Dispatcher
from create_bot import dp


# Тест по говнокоду)
# @dp.message_handler()
async def ask_govnokod(message : types.Message):
    if message.text == "Кто пишет говнокод?":
        await message.answer("Кто спрашивает тот и пишет")
        await message.answer("И вообще, выключи компьютер!")

    else:
        await message.answer("Я тебя не понимаю!")


# Передача остальных команд
def register_handlers_other(dp : Dispatcher):

    dp.register_message_handler(ask_govnokod)
