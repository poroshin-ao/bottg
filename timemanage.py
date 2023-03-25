from bot_space import dp, scheduler, Dispatcher, time_format, bot
from datetime import datetime, timedelta
from datafunc import get_quests, get_keys_quest, get_keys_users, set_open_quest
from datafunc import set_open_pods, get_answers


async def open_quest(dp: Dispatcher, name: str):
    k = get_keys_users()
    set_open_quest(name)
    for i in k:
        await bot.send_message(i, f"Открыто задание {name}. Приступайте.")
    return


async def open_pods(dp: Dispatcher, name: str):
    a = get_answers()
    k = get_keys_users()
    set_open_pods(name)
    for i in k:
        if not a.get(i, None):
            await bot.send_message(i, f"Теперь вы можете воспользоваться подсказкой для задания {name}")
        elif not a.get(i).get(name, None):
            await bot.send_message(i, f"Теперь вы можете воспользоваться подсказкой для задания {name}")
    return


def schedule_add_jobs(name: dict, dat):
    dat1 = dat+timedelta(hours=-4)
    scheduler.add_job(open_quest, "date", run_date=dat1, args=(dp, name))


def schedule_add_jobs_pods(name: dict, dat):
    n = datetime.now()
    dat1 = dat+timedelta(hours=20-4)
    if dat1 <= n:
        set_open_pods(name)
    scheduler.add_job(open_pods, "date", run_date=dat1, args=(dp, name))


async def last_word(dp: Dispatcher):
    k = get_keys_users()
    for i in k:
        await bot.send_message(i, "Экзамен окончен. Ответы в зачёт больше не принимаются. Если Вы оказались в числе лучших, мы с Вами свяжемся – ждите сообщения в ВК. Ваши личные сообщения должны быть открыты.")
    return


def scheduler_start():
    scheduler.add_job(last_word, "date", run_date=datetime.strptime('31/03/23 20:00', time_format))
    q = get_quests()
    k = get_keys_quest()
    for i in k:
        if not q.get(i).get('open', None) and q.get(i).get('date', None):
            schedule_add_jobs(i, datetime.strptime(q.get(i).
                                                   get('date', None),
                                                   time_format))
        if not q.get(i).get('open_pods', None):
            schedule_add_jobs_pods(i, datetime.strptime(q.get(i).
                                                        get('date', None),
                                                        time_format))
    scheduler.start()
