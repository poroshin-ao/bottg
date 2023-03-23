from bot_space import dp, scheduler, Dispatcher, time_format, bot
from datetime import datetime, timedelta
from datafunc import get_quests, get_keys_quest, get_keys_users, set_open_quest
from datafunc import set_open_pods, get_answers


async def open_quest(dp: Dispatcher, name: str):
    k = get_keys_users()
    set_open_quest(name)
    for i in k:
        await bot.send_message(i, f"Открыто задание {name}")
    return


async def open_pods(dp: Dispatcher, name: str):
    a = get_answers()
    k = get_keys_users()
    set_open_pods(name)
    for i in k:
        if not a.get(i, None):
            await bot.send_message(i, f"Открыта подсказка для {name}")
        elif not a.get(i).get(name, None):
            await bot.send_message(i, f"Открыта подсказка для {name}")
    return


def schedule_add_jobs(name: dict, dat):
    scheduler.add_job(open_quest, "date", run_date=dat, args=(dp, name))


def schedule_add_jobs_pods(name: dict, dat):
    n = datetime.now()
    dat1 = dat+timedelta(hours=20)
    if dat1 <= n:
        set_open_pods(name)
    scheduler.add_job(open_pods, "date", run_date=dat1, args=(dp, name))


def scheduler_start():
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
