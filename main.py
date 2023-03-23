from aiogram.utils import executor
from bot_space import dp
from timemanage import scheduler_start
from handlers import client, other, admin, registration, admin_menu, quests
from handlers import pods


async def on_startup(_):
    print('Работаем!')


admin.register_handler_admin(dp)
client.register_handlers_client(dp)
registration.register_handlers_registration(dp)
pods.register_handlers_pods(dp)
quests.register_handlers_quests(dp)
admin_menu.register_handlers_admin_menu(dp)
other.register_handlers_other(dp)

scheduler_start()
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
