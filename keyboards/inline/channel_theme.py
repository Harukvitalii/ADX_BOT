
from cgitb import text
from tabnanny import check
from .callback_data import theme_callback
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




def channel_theme(themes):
    channel_theme = InlineKeyboardMarkup(row_width=2)
    row_btns = (InlineKeyboardButton(text=key, callback_data=f'theme:{value}') for key, value in themes.items())
    channel_theme.add(*row_btns)
    return channel_theme


def change_channel_theme(themes):
    channel_theme = InlineKeyboardMarkup(row_width=2)
    row_btns = (InlineKeyboardButton(text=key, callback_data=f'change_th:{value}') for key, value in themes.items())
    channel_theme.add(*row_btns)
    channel_theme.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_btn'))
    return channel_theme

def banned_theme_callback(th, check_btns = None):
    if check_btns != None:
        for banned in check_btns:
            th[banned] = '🦋'
        for k,v in th.items():
            if v == '🦋' and k not in check_btns:
                th[k] = k
    channel_theme = InlineKeyboardMarkup(row_width=2)
    row_btns = (InlineKeyboardButton(text=value, callback_data=f'banned:{key}') for key, value in th.items())
    channel_theme.add(*row_btns)
    next = InlineKeyboardButton(text='Готово', callback_data=f'baned_next')
    channel_theme.row(next)
    return channel_theme

