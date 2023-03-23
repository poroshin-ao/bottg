from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from bot_space import bot, admins
from keyboards import kb_admin_menu, kb_admin_delete
from datafunc import delete_quests, delete_users


class FSMAdminDelete(StatesGroup):
    delgroup = State()


async def del_start(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    await FSMAdminDelete.delgroup.set()
    await bot.send_message(message.from_user.id, 'Что нужно удалить?',
                           reply_markup=kb_admin_delete)


async def delete_any(message: types.Message, state: FSMContext):
    if message.text == 'Участников':
        delete_users()
        await bot.send_message(message.from_user.id, 'Участники удалены',
                               reply_markup=kb_admin_menu)
    if message.text == 'Задания':
        delete_quests()
        await bot.send_message(message.from_user.id, 'Задания удалены',
                               reply_markup=kb_admin_menu)
    if message.text == 'Вернуться':
        await bot.send_message(message.from_user.id, 'ok',
                               reply_markup=kb_admin_menu)

    await state.finish()


def register_handler_admin_delete(dp: Dispatcher):
    dp.register_message_handler(del_start, commands=['Удалить'],
                                state=None)
    dp.register_message_handler(delete_any, state=FSMAdminDelete.delgroup)
