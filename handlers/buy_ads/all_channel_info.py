from random import randint
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import pgbotdb,dp
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, InputMediaPhoto
import json
sort_channels_callback = CallbackData('all_channels', 'act', 'page', "sort_by", 'reverse')
channel_info_callback = CallbackData('channel_info', 'id', 'page', "sort_by", 'reverse')

async def channel_info_call(call: CallbackQuery, data: CallbackData):
    edit_kb = False
    sort_by = data['sort_by']
    reverse = data['reverse']
    page = data['page']
    id = data['id']
    if '$nt' in id:
        id = get_next_id(id, sort_by,reverse)
        edit_kb = True

    channel_info = pgbotdb.select_channel(channel_id=id)
    channel_statistics = pgbotdb.select_channel_statistic_today(id)
    channel_conditions = pgbotdb.get_conditions(id)
    

    kb = InlineKeyboardMarkup(row_width=4)

    btns=(InlineKeyboardButton(text=time,callback_data='buy_s_time$' + str(id) + '$' +time) for time,price in channel_conditions)
    kb.add(*btns)
    kb.row(InlineKeyboardButton("Назад", callback_data=sort_channels_callback.new('BACK',data['page'], data['sort_by'], data['reverse'])))
    
    kb.insert(InlineKeyboardButton(text=' ___ ', callback_data='незнаю'))
    kb.insert(InlineKeyboardButton(text='NEXT', callback_data=channel_info_callback.new(str(id)+'$nt',page, sort_by, reverse)))


    forbidden_themes = forbid_theme(json.loads(channel_info[8]))
    caption = f"""Ссылка на канал: 🦋 <a href='{channel_info[4]}'>{channel_info[3]}</a> 🦋
Запрещенные тематики: {forbidden_themes}
Тематика: {channel_info[7]}
Подписчиков: {channel_statistics[3]} чел.
Условия: {' '.join(map(condition, channel_conditions))}
Цена за 1000 views: ~{channel_statistics[-1]} руб
Комментарий: {channel_info[6]}
"""

    img_link = pgbotdb.get_channel_stat_img(channel_info[1])
    print(f'image_link = ,{img_link},', )
    if edit_kb:
        await dp.bot.edit_message_media(chat_id=call.from_user.id, message_id=call.message.message_id,
        media=InputMediaPhoto(media=img_link))
        await dp.bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.message_id,
        caption=caption,
        reply_markup=kb)
    else:
        await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        
        await dp.bot.send_photo(
            chat_id=call.message.chat.id,
            photo=img_link,
            caption=caption,
            parse_mode="HTML",
            reply_markup=kb
        )








def forbid_theme(theme:list):
    string = ''
    if len(theme) == 0:
        return 'Нет'
    for i in theme:
        string = string + i
    return string


def condition(cond :list)->str:
    string = '\n' + str(cond[0]) + ' - ' + str(cond[1]) + ' руб'
    return string

def get_next_id(id_with_next, sort_by, reverse):
    id_prev = id_with_next.replace('$nt', '')
    statistics = pgbotdb.select_all_channel_statistics_today()
    sorted_list = []
    if sort_by == "ERR":
        sorted_list = sorted(statistics, key=lambda err: err[10])
    elif sort_by == "CPV":
        sorted_list = sorted(statistics, key=lambda cpv: cpv[11])
    elif sort_by == "ПДП":
        sorted_list = sorted(statistics, key=lambda sub: sub[3])
    
    if reverse=='True':
        sorted_list.reverse()
    print(id_prev, type(id_prev))
    for i in range(0,len(sorted_list)):
        # print(i)
        # print(sorted_list[i][1], type(sorted_list[i][1]))
        if int(id_prev) == sorted_list[i][1]:
            try:
                print("next", sorted_list[i+1][1])
            except IndexError:
                return sorted_list[0][1]
            return sorted_list[i+1][1]
