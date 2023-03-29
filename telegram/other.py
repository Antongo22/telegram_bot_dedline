from aiogram import types, Dispatcher
from create_bot import dp


async def ask_govnokod(message: types.Message):  # Посхалка от разраба + обработка неправильного ответа от пользователя
    if message.text.lower() == "кто пишет говнокод?":
        await message.answer("Кто спрашивает тот и пишет")
        await message.answer("И вообще, выключи компьютер!")

    else:
        await message.answer("Я тебя не понимаю!")


def register_handlers_other(dp: Dispatcher):  # Передача остальных команд
    dp.register_message_handler(ask_govnokod)