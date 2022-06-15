from aiogram import executor
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from adx_graph.main import make_post_stat

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    # await make_post_stat('https://t.me/adx_me',26)
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)

