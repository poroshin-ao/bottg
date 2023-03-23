from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
b1 = KeyboardButton('/Участники')
b2 = KeyboardButton('/Добавить_задание')
b3 = KeyboardButton('/start')
kb_admin_menu.add(b1).add(b2).add(b3)
