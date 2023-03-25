from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import ReplyKeyboardRemove


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/Информация')
b2 = KeyboardButton('/Регистрация')
kb_client.insert(b1).insert(b2)
# .add(b1).row(b1,b1)


kb_close = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/Отмена')
kb_close.insert(b1)


kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/Информация')
b2 = KeyboardButton('/Профиль')
b3 = KeyboardButton('/Помощь')
b4 = KeyboardButton('/Задания')
kb_menu.insert(b1).insert(b2).insert(b4).insert(b3)


kb_profile = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/Изменить_профиль')
b2 = KeyboardButton('/Меню')
kb_profile.insert(b1).insert(b2)
