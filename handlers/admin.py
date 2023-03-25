from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_space import bot, admins, time_format
from keyboards import kb_menu, kb_client, kb_close, kb_admin_menu
from datafunc import exist_id, set_new_quest
from timemanage import schedule_add_jobs, schedule_add_jobs_pods
from datetime import datetime


class FSMAdmin(StatesGroup):
    name = State()
    robot = State()
    text = State()
    otvet = State()
    needs = State()
    photo = State()
    video = State()
    open = State()
    dat = State()
    podskaz_chek = State()
    podskaz = State()


# @dp.message_handler(commands = "Загрузить", state = None)
async def cm_start(message: types.Message):
    if str(message.from_user.id) not in admins:
        return

    await FSMAdmin.name.set()
    await bot.send_message(message.from_user.id, 'Напиши название задания',
                           reply_markup=kb_close)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Это задание с бинарным поиском?(Да/Нет)")


async def load_robot(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            data['robot'] = True
    await FSMAdmin.next()
    await message.reply("Введите текст задания")


# @dp.message_handler(state = FSMAdmin.name)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await FSMAdmin.next()
    await message.reply("Теперь введи ответ на тест")


# @dp.message_handler(state = FSMAdmin.otvet)
async def load_otvet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['otvet'] = message.text

    await FSMAdmin.next()
    await message.reply('Нужно ли (Фото/Видео/Нет)?')


# @dp.message_handler(content_types = ['photo'], state = FSMAdmin.photo)
async def it_needs(message: types.Message, state: FSMContext):
    r = message.text.lower()
    if r == 'фото':
        await FSMAdmin.photo.set()
        await message.reply("Вставте фото")
        return
    if r == 'видео':
        await FSMAdmin.photo.set()
        await message.reply("Вставте видео")
        return

    await FSMAdmin.open.set()
    await message.reply("Нужно ли открыть его после загрузки?(Да/Нет)")


# @dp.message_handler(content_types = ['photo'], state = FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        print(dict(data))
    await FSMAdmin.open.set()
    await message.reply("Нужно ли открыть его после загрузки?(Да/Нет)")


async def load_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.video.file_id
    await FSMAdmin.open.set()
    await message.reply("Нужно ли открыть его после загрузки?(Да/Нет)")


async def load_open(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            data['open'] = True

    else:
        async with state.proxy() as data:
            data['open'] = False

    await FSMAdmin.podskaz_chek.set()
    await message.reply("Нужна ли подсказка? Она будет открыта через 20 часов\
                        после задания (Да/Нет)")


async def check_podskaz(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            data['open_pods'] = False

            await FSMAdmin.podskaz.set()
            await message.reply("Введите подсказку")
            return

        elif not data['open']:
            await FSMAdmin.dat.set()
            await message.reply(f"Введите дату в формате {time_format} \
                            (пример 20/03/23 12:27)")
            return

    async with state.proxy() as data:
        d = dict(data)
        name = d['name']
        d.pop('name')
        q = {name: dict(d)}
        set_new_quest(q)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Задание добавлено',
                           reply_markup=kb_admin_menu)


async def load_podskaz(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pods'] = message.text

    await FSMAdmin.dat.set()
    await message.reply(f"Введите дату в формате {time_format} \
                            (пример 20/03/23 12:27)")


async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            date_time = datetime.strptime(message.text, time_format)
        except ValueError:
            await message.reply("Не првильный формат, попробуй ещё раз")
            return
        d = dict(data)
        name = d['name']
        d['date'] = message.text
        d.pop('name')
        q = {name: dict(d)}
        set_new_quest(q)
        schedule_add_jobs(data['name'], date_time)
        schedule_add_jobs_pods(data['name'], date_time)

    await state.finish()
    await bot.send_message(message.from_user.id, 'Задание добавлено',
                           reply_markup=kb_admin_menu)


# @dp.message_handler(state="*",commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id, 'Отмена действия',
                               reply_markup=kb_menu)
    else:
        await bot.send_message(message.from_user.id, 'Отмена действия',
                               reply_markup=kb_client)


async def otmena(message: types.Message):

    await bot.send_message(message.from_user.id, 'Отмена', 
                           reply_markup=kb_menu)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Добавить_задание'],
                                state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_robot, state=FSMAdmin.robot)
    dp.register_message_handler(it_needs, state=FSMAdmin.needs)
    dp.register_message_handler(load_open, state=FSMAdmin.open)
    dp.register_message_handler(load_date, state=FSMAdmin.dat)
    dp.register_message_handler(check_podskaz, state=FSMAdmin.podskaz_chek)
    dp.register_message_handler(load_podskaz, state=FSMAdmin.podskaz)
    dp.register_message_handler(load_photo, content_types=['photo'],
                                state=FSMAdmin.photo)
    dp.register_message_handler(load_video, content_types=['video'],
                                state=FSMAdmin.photo)
    dp.register_message_handler(load_text, state=FSMAdmin.text)
    dp.register_message_handler(load_otvet, state=FSMAdmin.otvet)
    dp.register_message_handler(otmena, commands=['Отмена'])
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='Отмена',
                                ignore_case=True), state="*")
    dp.register_message_handler(cancel_handler, Text(equals='Отмена',
                                ignore_case=True))
    dp.register_message_handler(cancel_handler, commands=['Отмена'])
