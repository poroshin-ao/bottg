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

info_text = "Что ж, раз Вы здесь, скорее всего, Вы чрезвычайно умны. А мы хотим убедиться в этом. Мы занимаемся изучением многих видов особых интеллектуальных аномалий, и нам нужны люди с высоким интеллектом, способные сделать мир лучше с помощью своего блестящего ума. Главный вопрос – окажетесь ли среди них Вы? Добро пожаловать на самый нестандартный экзамен в Вашей жизни.\n\n"
info_text = info_text + "Вам предстоит решить 5 составленных нами заданий и столкнуться с несколькими разными аномалиями (любые совпадения с реально существующими объектами случайны). Первое задание станет доступно в понедельник, 27 марта, ровно в полночь. Каждое последующее будет открываться ровно через сутки после предыдущего. Всё просто: успейте дать максимальное число правильных ответов до 00:00 субботы, 1 апреля, и, может быть, Вы окажетесь в числе лидеров.\n\n"
info_text = info_text + "Чтобы мы могли отслеживать Ваш прогресс, пройдите регистрацию. Пожалуйста, вводите свои настоящие данные. В противном случае нам придётся дисквалифицировать Вас. Не переживайте – никто, кроме высшей инстанции, не сможет узнать информацию о Вас.\n\n"
info_text = info_text + "У Вас будет неограниченное число попыток ответить на каждое задание. Не переживайте, если поначалу не сможете справиться с каким-то заданием, – каждый день будут открываться новые, которые могут оказаться Вам под силу и вывести Вас в лидеры испытания, а все открытые задания можно будет решать до самого конца экзамена. Также предусмотрена система помощи: через некоторое время после открытия очередного задания у Вас будет появляться возможность воспользоваться подсказкой к нему. Однако это Ваш выбор – можно не открывать появившуюся подсказку и прийти к ответу самостоятельно.\n\n" 
info_text = info_text + "Пока в разделах «Задания» и «Помощь» ничего нет, но мы будем уведомлять Вас об открывшихся заданиях или появившихся возможностях воспользоваться подсказкой; в разделах также появятся соответствующие кнопки. Уведомления приходят только зарегистрированным пользователям. Чтобы открыть панель кнопок, нажмите на плитку справа в окне ввода сообщения.\n\n"
info_text = info_text + "По любым техническим вопросам обращайтесь в личные сообщения паблика ВКонтакте Информер МЦ ИМиФИ (vk.com/imfi_sfu)."
