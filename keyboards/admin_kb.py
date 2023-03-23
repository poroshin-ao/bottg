from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
b1 = KeyboardButton('/Участники')
b11 = KeyboardButton('/Победители')
b2 = KeyboardButton('/Добавить_задание')
b22 = KeyboardButton('/Все_задания')
b3 = KeyboardButton('/start')
b4 = KeyboardButton('/Удалить')
kb_admin_menu.add(b1).add(b11).add(b2).add(b22).add(b3).add(b4)


kb_admin_delete = ReplyKeyboardMarkup(resize_keyboard=True,
                                      one_time_keyboard=True)
b1 = KeyboardButton('Участников')
b2 = KeyboardButton('Задания')
b3 = KeyboardButton('Вернуться')
kb_admin_delete.add(b1).add(b2).add(b3)
