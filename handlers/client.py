from bot_space import bot
from aiogram import types, Dispatcher
from keyboards import kb_client, kb_menu, kb_profile
from datafunc import exist_id, get_user, get_answer, get_keys_quest, get_quests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):

    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               "Это ваше меню",
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id,
                               "Ты круче некуда! Но не зареган!",
                               reply_markup=kb_client)


async def command_info(message: types.Message):
    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               "Ты круче некуда! Зареган",
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id,
                               "Ты круче некуда! Но не зареган!",
                               reply_markup=kb_client)


async def command_profile(message: types.Message):
    if exist_id(str(message.from_user.id)):
        user = get_user(str(message.from_user.id))
        s = f"Ваши данные:\n\n{user.get('famname')}\n" + \
            f"{user.get('institute')}\n\nВремя выполения заданий:\n"
        ans = get_answer(str(message.from_user.id))
        if ans:
            for i in ans:
                s += f"{i}: {ans.get(i)}\n"
        else:
            s += "К сожалению в ничего не прошли"
        await bot.send_message(message.from_user.id, s,
                               reply_markup=kb_profile)
    else:
        await bot.send_message(message.from_user.id,
                               "Ты круче некуда! Но не зареган!",
                               reply_markup=kb_client)


async def command_pods(message: types.Message):
    if exist_id(str(message.from_user.id)):
        k = get_keys_quest()
        q = get_quests()

        kb_quests = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)

        for i in k:
            if q.get(i).get('open'):
                b = KeyboardButton(i)
                kb_quests.add(b)

        await bot.send_message(message.from_user.id, "",
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id,
                               "Ты круче некуда! Но не зареган!",
                               reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Старт',
                                                         'Меню'])
    dp.register_message_handler(command_start, Text(equals='Отмена',
                                ignore_case=True))
    dp.register_message_handler(command_info, commands=['Информация'])
    dp.register_message_handler(command_profile, commands=['Профиль'])
