from bot_space import bot, admins
from aiogram import types, Dispatcher
from keyboards import kb_admin_menu
from datafunc import get_users, get_keys_users, get_answers


async def command_admin(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    await bot.send_message(message.from_user.id, "Здаров, админ",
                           reply_markup=kb_admin_menu)


async def command_users(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    k = get_keys_users()
    u = get_users()
    ans = get_answers()

    for i in k:
        s = f"{i}\n{u.get(i).get('famname')}\n{u.get(i).get('institute')}\n\n"
        key = ans.get(i)
        if key:
            for a in key.keys():
                s += f"{a}: {key.get(a,None)}\n"
        await bot.send_message(message.from_user.id, s)

    await bot.send_message(message.from_user.id, "Это всё!",
                           reply_markup=kb_admin_menu)


def register_handlers_admin_menu(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['Админ'])
    dp.register_message_handler(command_users, commands=['Участники'])
