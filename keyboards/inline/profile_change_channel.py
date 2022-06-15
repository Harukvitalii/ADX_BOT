from loader import pgbotdb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import my_channels_callback


def my_channels(admin_id: str, prefix = 'change_chnl'):
    channels_id = pgbotdb.select_channels_for_del(admin_id=admin_id)

    kb = InlineKeyboardMarkup(row_width=1)
    for channel in channels_id:
        if prefix == 'change_chnl':
            kb_btn = InlineKeyboardButton(text=channel[0], callback_data=f'change_chnl:1:{channel[1]}:row')   
        else: kb_btn = InlineKeyboardButton(text=channel[0], callback_data=f'{prefix}:{channel[1]}')   
        kb.add(kb_btn)
    if prefix == 'change_chnl':
        kb.add(InlineKeyboardButton('Назад', callback_data='back_to_channels'))
    else: kb.add(InlineKeyboardButton('Назад', callback_data='my_channels'))
    return kb

def admin_del_channels(prefix = 'change_chnl'):
    channels_id = pgbotdb.select_all_channels_for_del()

    kb = InlineKeyboardMarkup(row_width=1)
    for channel in channels_id:
        if prefix == 'change_chnl':
            kb_btn = InlineKeyboardButton(text=channel[0], callback_data=f'change_chnl:1:{channel[1]}:row')   
        else: kb_btn = InlineKeyboardButton(text=channel[0], callback_data=f'{prefix}:{channel[1]}')   
        kb.add(kb_btn)
    if prefix == 'change_chnl':
        kb.add(InlineKeyboardButton('Назад', callback_data='back_to_channels'))
    else: kb.add(InlineKeyboardButton('Назад', callback_data='my_channels'))
    return kb




def change_channel_parameters(channel_id):
    kb = InlineKeyboardMarkup(row_width=3)
    parameters = ['name', 'link', "description", 'comment', "channels_theme", "change-baned_theme", 'times_for_posts']
    parameters = [["Имя", 'name'], ["Ссылка",'link'], ["Описание", "description"], ["Комментарий", 'comment'], ["Тематика","channels_theme"], ['Запрещение тематики', "change-baned_theme"], ["Время постов", 'times_for_posts'], ["Ценник",'conditions']]
    btns = (InlineKeyboardButton(text = param[0], callback_data=my_channels_callback.new(
        lvl=2,
        channel_id = channel_id,
        row=param[1]
    )) for param in parameters)
    kb.add(*btns)
    kb.add(InlineKeyboardButton('Назад', callback_data='back_to_my_channels'))
    return kb

def back_to_channel_rows(channel_id):
    kb = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[ 
        [InlineKeyboardButton('Готово', callback_data="back_to_my_channels")],
        [InlineKeyboardButton('Назад', callback_data=f"b_t_s_c:{channel_id}")],
        ])
    return kb

def change_channel_row():
    pass
