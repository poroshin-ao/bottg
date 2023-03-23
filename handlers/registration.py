from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_space import bot
from aiogram import types, Dispatcher
from datafunc import set_new_user, exist_id
from keyboards import kb_close, kb_menu


class FSMRegistration(StatesGroup):
    famname = State()
    institute = State()


async def reg_start(message: types.Message):
    if exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               'Вы уже были зарегистрированны!')
        return
    await FSMRegistration.famname.set()
    await bot.send_message(message.from_user.id, 'Напиши своё имя и фамилию',
                           reply_markup=kb_close)


async def reg_fi(message: types.Message, state: FSMContext):
    if len(message.text) > 40:
        await bot.send_message(message.from_user.id,
                               'Похоже вы ошиблись в написании своего имени и фамилии. Попробуйте ещё раз')
        return

    async with state.proxy() as data:
        data['famname'] = message.text
    await FSMRegistration.next()
    await bot.send_message(message.from_user.id, 'Напиши свой институт')


async def reg_institute(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['institute'] = message.text
        r = {str(message.from_user.id): dict(data)}
        set_new_user(r)
    await state.finish()

    await bot.send_message(message.from_user.id, 'Регистрация прошла успешно',
                           reply_markup=kb_menu)


async def reg_rereg(message: types.Message, state: FSMContext):
    if not exist_id(str(message.from_user.id)):
        await bot.send_message(message.from_user.id,
                               'Вы не были зарегистрированны ранее')
        return
    await FSMRegistration.famname.set()
    await bot.send_message(message.from_user.id, 'Напиши своё имя и фамилию',
                           reply_markup=kb_close)


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(reg_start, commands='Регистрация', state=None)
    dp.register_message_handler(reg_fi, state=FSMRegistration.famname)
    dp.register_message_handler(reg_institute, state=FSMRegistration.institute)
    dp.register_message_handler(reg_rereg, commands='Изменить_профиль',
                                state=None)
