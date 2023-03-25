from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler


admins = ['405489476', '1886795974']
time_format = f"%d/%m/%y %H:%M{''}"
storage = MemoryStorage()

TOKEN = '6110253917:AAEQxqHDOKxz_DrSOjA8P7x40zzXKB392io'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler()

info_text = ""
