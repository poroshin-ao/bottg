from bot_space import bot, admins
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards import kb_admin_menu
from datafunc import get_users, get_keys_users, get_answers, get_keys_quest, get_quests


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


async def command_win_users(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    k = get_keys_users()
    u = get_users()
    ans = get_answers()
    q = get_keys_quest()

    for i in k:
        key = ans.get(i, None)
        f = 0
        if key:
            for a in q:
                if not key.get(a, None):
                    f = 1
                    break
        else:
            continue
        if f:
            continue
        s = f"{i}\n{u.get(i).get('famname')}\n{u.get(i).get('institute')}\n\n"
        if key:
            for a in key.keys():
                s += f"{a}: {key.get(a,None)}\n"
        await bot.send_message(message.from_user.id, s)

    await bot.send_message(message.from_user.id, "Это всё!",
                           reply_markup=kb_admin_menu)


class FSMAdminQuests(StatesGroup):
    quests = State()


async def start_quest(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    kb_quests = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
    k = get_keys_quest()
    for i in k:
        b = KeyboardButton(i)
        kb_quests.insert(b)
    b = KeyboardButton('Вернуться')
    kb_quests.insert(b)

    await FSMAdminQuests.quests.set()
    await bot.send_message(message.from_user.id, 'Жмякни на кнопку задания',
                           reply_markup=kb_quests)


async def quest_h(message: types.Message, state: FSMContext):
    k = get_keys_quest()
    if message.text not in k and message.text != 'Вернуться':
        return

    if message.text == 'Вернуться':
        await bot.send_message(message.from_user.id, "ok",
                               reply_markup=kb_admin_menu)
        await state.finish()
        return

    q = get_quests()

    qst = q.get(message.text)
    photo = qst.get('photo', None)
    video = qst.get('video', None)
    text = qst.get('text')
    otvet = qst.get('otvet')
    robot = qst.get('robot', False)

    if photo:
        await bot.send_photo(message.from_user.id, photo)

    if video:
        await bot.send_video(message.from_user.id, video)

    mes = f"{message.text}\nОтвет: {otvet}\nРобот: {robot}\n\n{text}"

    await bot.send_message(message.from_user.id, mes,
                           reply_markup=kb_admin_menu)
    await state.finish()


def register_handlers_admin_menu(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['Админ'])
    dp.register_message_handler(command_win_users, commands=['Победители'])
    dp.register_message_handler(command_users, commands=['Участники'])
    dp.register_message_handler(start_quest, commands=['Все_задания'],
                                state=None)
    dp.register_message_handler(quest_h, state=FSMAdminQuests.quests)
