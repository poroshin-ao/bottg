from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from bot_space import bot
from keyboards import kb_client, kb_menu
from datafunc import exist_id, get_keys_quest, get_quests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class FSMPods(StatesGroup):
    pods = State()


async def pods_menu(message: types.Message):
    if exist_id(str(message.from_user.id)):
        k = get_keys_quest()
        q = get_quests()

        kb_pods = ReplyKeyboardMarkup(resize_keyboard=True,
                                      one_time_keyboard=True)

        for i in k:
            if q.get(i).get('open_pods', None):
                b = KeyboardButton(i)
                kb_pods.insert(b)
        kb_pods.insert('Отмена')
        await FSMPods.pods.set()
        await bot.send_message(message.from_user.id, "Помощь на задания",
                               reply_markup=kb_pods)
    else:
        await bot.send_message(message.from_user.id,
                               "Вы не были зарегистрированны ранее",
                               reply_markup=kb_client)


async def print_pods(message: types.Message, state: FSMContext):
    q = get_quests()

    if q.get(message.text, None):
        if q.get(message.text).get('open_pods', None):
            await state.finish()
            await bot.send_message(message.from_user.id,
                                   q.get(message.text).get('pods', None),
                                   reply_markup=kb_menu)
        else:
            await bot.send_message(message.from_user.id,
                                   "Такое чувство буд-то вы куда-то спешите")
    else:
        await bot.send_message(message.from_user.id,
                               "Такого задания не существует (нажмите отмена)")


def register_handlers_pods(dp: Dispatcher):
    dp.register_message_handler(pods_menu, commands='Помощь', state=None)
    dp.register_message_handler(print_pods, state=FSMPods.pods)
