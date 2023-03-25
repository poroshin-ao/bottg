import json
import datetime


def get_users():
    r = json.load(open('users.json', encoding='utf-8'))
    r = json.loads(r)
    return r


def set_new_user(usr: dict):
    d = get_users()
    d.update(usr)
    dj = json.dumps(d)
    json.dump(dj, open('users.json', 'w', encoding='utf-8'))


def get_keys_users():
    d = get_users()
    return list(d.keys())


def exist_id(id: str):
    return id in get_keys_users()


def get_user(id: str):
    return get_users().get(id)


def get_quests():
    r = json.load(open('quests.json', encoding='utf-8'))
    r = json.loads(r)
    return r


def get_quest(name: str):
    return get_quests().get(name)


def get_keys_quest():
    d = get_quests()
    return list(d.keys())


def set_new_quest(q: dict):
    d = get_quests()
    d.update(q)
    dj = json.dumps(d)
    json.dump(dj, open('quests.json', 'w', encoding='utf-8'))


def set_open_quest(name: dict):
    d = get_quests()
    d[name]['open'] = True
    dj = json.dumps(d)
    json.dump(dj, open('quests.json', 'w', encoding='utf-8'))


def get_answers():
    r = json.load(open('correct_answer.json', encoding='utf-8'))
    r = json.loads(r)
    return r


def get_answer(id: str):
    return get_answers().get(id, None)


def set_new_correct_answer(id: str, name: str):
    d = get_answers()
    u = d.get(id, None)
    now = datetime.datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
    if u:
        if u.get(name, None):
            return
        u.update({name: t})
        d.update(u)
    else:
        q = {id: {name: t}}
        d.update(q)
    dj = json.dumps(d)
    json.dump(dj, open('correct_answer.json', 'w', encoding='utf-8'))


def set_open_pods(name: str):
    q = get_quests()
    if q.get(name, None):
        q[name].update({'open_pods': True})
    dj = json.dumps(q)
    json.dump(dj, open('quests.json', 'w', encoding='utf-8'))


def delete_quests():
    dj = json.dumps({})
    json.dump(dj, open('quests.json', 'w', encoding='utf-8'))
    json.dump(dj, open('correct_answer.json', 'w', encoding='utf-8'))


def delete_users():
    dj = json.dumps({})
    json.dump(dj, open('users.json', 'w', encoding='utf-8'))
    json.dump(dj, open('correct_answer.json', 'w', encoding='utf-8'))
