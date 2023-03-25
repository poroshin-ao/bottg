from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from bot_space import bot
from keyboards import kb_close, kb_client, kb_menu
from datafunc import exist_id, get_keys_quest, get_quests
from datafunc import set_new_correct_answer
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from robot import str_to_robot


class FSMQuests(StatesGroup):
    quest = State()
    quest_insert = State()


async def quest_menu(message: types.Message):
    if not exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               'Вы не были зарегистрированны ранее',
                               reply_markup=kb_client)
        return

    kb_quests = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
    k = get_keys_quest()
    q = get_quests()
    for i in k:
        if q.get(i).get('open'):
            b = KeyboardButton(i)
            kb_quests.insert(b)
    b = KeyboardButton('Отмена')
    kb_quests.insert(b)

    await FSMQuests.quest.set()
    await bot.send_message(message.from_user.id, 'Выберите задание',
                           reply_markup=kb_quests)


async def quest(message: types.Message, state: FSMContext):

    k = get_keys_quest()

    if message.text not in k:
        await bot.send_message(message.from_user.id, 'Такого задания нет')
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

    await bot.send_message(message.from_user.id, f"{message.text}\n\n{text}")

    async with state.proxy() as data:
        data['otvet'] = otvet
        data['robot'] = robot
        data['name'] = message.text

    await FSMQuests.quest_insert.set()
    await bot.send_message(message.from_user.id, 'Введите ответ',
                           reply_markup=kb_close)


async def quest_insert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        otvet = data['otvet']
        robot = data['robot']
        name = data['name']

    if message.text.lower() == otvet.lower():
        set_new_correct_answer(str(message.from_user.id), name)
        await state.finish()
        await bot.send_message(message.from_user.id, 'Поздравляем, Ваш ответ верный.\nПродолжайте в том же духе.',
                               reply_markup=kb_menu)
        return

    if robot:
        await bot.send_message(message.from_user.id, str_to_robot(message.text,
                                                                  otvet))
    else:
        await bot.send_message(message.from_user.id, 'Ваш ответ неверный.\nПопробуйте ещё раз.')


def register_handlers_quests(dp: Dispatcher):
    dp.register_message_handler(quest_menu, commands='Задания', state=None)
    dp.register_message_handler(quest, state=FSMQuests.quest)
    dp.register_message_handler(quest_insert, state=FSMQuests.quest_insert)
