from loader import dp, pgbotdb
from aiogram.types.callback_query import CallbackQuery
from keyboards.inline import my_channels, del_channel_markup,admin_del_channels
from data.config import ADMIN

@dp.callback_query_handler(text='del_channel')
async def del_channel(call: CallbackQuery):
    if int(call.from_user.id) == int(ADMIN):
        await call.message.edit_text(text='🦋Ваши канали', reply_markup=admin_del_channels(prefix='delete_my_channel'))
    else:
        await call.message.edit_text(text='🦋Ваши канали', reply_markup=my_channels(call.from_user.id, prefix='delete_my_channel'))


@dp.callback_query_handler(text_contains='delete_my_channel')
async def del_channel(call: CallbackQuery):
    channel_id = call.data.split(":")[1]
    channel = pgbotdb.select_channel(channel_id)
    print(channel)
    await call.message.edit_text(f'Вы действительно хотите удалить канал: {channel[3]}', reply_markup=del_channel_markup(channel_id))


@dp.callback_query_handler(text_contains='yes_del_my_channel')
async def yes_del_my_channel(call: CallbackQuery):
    channel_id = call.data.split(":")[1]
    pgbotdb.delete_channel(channel_id)
    await call.message.edit_text(f'Канал был удален :(')


dp.callback_query_handler(text='back_to_del_channels')
async def back_to_del_channels(call: CallbackQuery):
    await call.message.edit_text(text='🦋Выберите канал для удаления', reply_markup=my_channels(call.from_user.id))