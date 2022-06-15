from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import Message, message
from data.config import ADMIN
from states.fsm_payments import FSMBTC_BANKER
from loader import dp, pgbotdb
from keyboards.kbs_buy_ads import buy_choose_category
from .theme_theme_chann_kb import THEME_CANNELS, theme_channels_callback
from.theme_channel_info_call import theme_channel_info_callback
from.theme_channel_info_call import channel_info_call

@dp.callback_query_handler(text = 'choose_category')
async def choose_category(call: CallbackQuery):
    await call.message.edit_text(text='Категории', reply_markup=buy_choose_category(call_prefix='dds_c'))

@dp.callback_query_handler(text = 'choose_category_from_theme')
async def choose_category(call: CallbackQuery):
    await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text='Категории', reply_markup=buy_choose_category(call_prefix='dds_c'))


@dp.callback_query_handler(text_contains='dds_c')
async def buy_adds_c(call: CallbackQuery):
    print(call.data)
    theme = call.data.replace("dds_c:", "").split(' ')[0]
    channel_info = pgbotdb.select_channels_by_theme(theme)
    statistics = pgbotdb.select_all_channel_statistics_today()
    stati_stics = []
    for ch_stat in statistics:
        for info in channel_info:
            if info[1] == ch_stat[1]:
                stati_stics.append(ch_stat)
    sorted_list = sorted(stati_stics, key=lambda err: err[10])
    print('theme handlers')

    await call.message.edit_text(text='1-средняя цена за 1000 просмотров, 2-ERR, Тема, Название канала',
    reply_markup=await THEME_CANNELS().theme_chann_kb(channel_statistics=sorted_list, theme=theme))


@dp.callback_query_handler(theme_channels_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    await THEME_CANNELS().process_selection(call, callback_data)


@dp.callback_query_handler(theme_channel_info_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    print(callback_data)
    user_id = call.from_user.id
    channel_id = callback_data['id']
    page = callback_data['page']
    sort_by = callback_data['sort_by']
    reverse = callback_data['reverse']
    theme = callback_data['theme']
    pgbotdb.update_user_back_from_times(user_id,channel_id, page, sort_by, reverse, theme)
    await channel_info_call(call, callback_data)



