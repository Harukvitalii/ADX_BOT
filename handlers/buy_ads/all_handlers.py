from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import Message, message
from data.config import ADMIN
from states.fsm_payments import FSMBTC_BANKER
from loader import dp, pgbotdb
from keyboards.kbs_buy_ads import buy_all_channels
from .All_Channels import ALL_CANNELS, sort_channels_callback
from .all_channel_info import channel_info_callback, channel_info_call

@dp.callback_query_handler(text = 'choose_all_channels')
async def choose_category(call: CallbackQuery):
    statistics = pgbotdb.select_all_channel_statistics_today()
    sorted_list = sorted(statistics, key=lambda err: err[10])
    await call.message.edit_text(text='1-средняя цена за 1000 просмотров, 2-ERR, Тема, Название канала',
    reply_markup=await ALL_CANNELS().all_chann_kb(channel_statistics=sorted_list))


@dp.callback_query_handler(sort_channels_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    await ALL_CANNELS().process_selection(call, callback_data)


@dp.callback_query_handler(channel_info_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    print(callback_data)
    user_id = call.from_user.id
    channel_id = callback_data['id']
    page = callback_data['page']
    sort_by = callback_data['sort_by']
    reverse = callback_data['reverse']
    theme = '-'
    pgbotdb.update_user_back_from_times(user_id,channel_id, page, sort_by, reverse,theme)
    await channel_info_call(call, callback_data)







