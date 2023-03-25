from bot_space import bot, info_text
from aiogram import types, Dispatcher
from keyboards import kb_client, kb_menu, kb_profile
from datafunc import exist_id, get_user, get_answer
from aiogram.dispatcher.filters import Text


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):

    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               "Это ваше меню",
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id,
                               info_text,
                               reply_markup=kb_client)


async def command_info(message: types.Message):
    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               info_text,
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id,
                               info_text,
                               reply_markup=kb_client)


async def command_profile(message: types.Message):
    if exist_id(str(message.from_user.id)):
        user = get_user(str(message.from_user.id))
        s = f"Ваши данные:\n\nФИ: {user.get('famname', None)}\n" + \
            f"Институт: {user.get('institute', None)}\n" + \
            f"Ссылка на ВК: {user.get('silka', None)}\n\nВремя выполения \
                заданий:\n"
        ans = get_answer(str(message.from_user.id))
        if ans:
            for i in ans:
                s += f"{i}: {ans.get(i)}\n"
        else:
            s += "У Вас пока нет решённых заданий"
        await bot.send_message(message.from_user.id, s,
                               reply_markup=kb_profile)
    else:
        await bot.send_message(message.from_user.id,
                               "Вы не были зарегистрированны ранее",
                               reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Старт',
                                                         'Меню'])
    dp.register_message_handler(command_start, Text(equals='Отмена',
                                ignore_case=True))
    dp.register_message_handler(command_info, commands=['Информация'])
    dp.register_message_handler(command_profile, commands=['Профиль'])
