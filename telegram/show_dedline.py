from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keybords import kb_client
from keybords import kb_show


class FSMShow(StatesGroup):  # Команда для показа дедлайна
    ded_choice = State()


async def show_ded(message: types.Message, state: FSMContext):  # Начало выполнения команды
    await FSMShow.ded_choice.set()
    async with state.proxy() as data:
        data['user_id'] = message.chat.id
    await message.reply('Вот ваши дедлайны:', reply_markup=kb_show)

    # Вывод из БД имён всех дедлайнов

    await message.answer('Введите номер дедлайна, которо вы хотите полностью просмотреть.')


async def cancel_handler(message: types.Message, state: FSMContext):  # Выход из показа дедлайна
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('ОК', reply_markup=kb_client)
    await state.finish()


async def load_choice(message: types.Message, state: FSMContext):  # Получение имени дедлайна и переход на описание

    async with state.proxy() as data:
        data['user_id'] = message.chat.id
        data['ded_choice'] = message.text
    await FSMShow.next()
    await message.reply('Вот подробная инфорация о дедлайне:')

    async with state.proxy() as data:
        await message.reply(str(data))
    await message.answer('Выходим в главную!', reply_markup=kb_client)

    await state.finish()


def register_handler_show_dedline(db: Dispatcher):  # Регистрация команд для передачи
    db.register_message_handler(show_ded, lambda message: 'показать' in message.text, state=None)
    db.register_message_handler(cancel_handler, state="*", commands='отмена')
    db.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    db.register_message_handler(load_choice, state=FSMShow.ded_choice)
