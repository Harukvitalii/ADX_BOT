from re import I
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def del_channel_markup(ch_id):
    del_channel_markup = InlineKeyboardMarkup(
        inline_keyboard=[ 
            [InlineKeyboardButton('Подтвердить', callback_data=f'yes_del_my_channel:{ch_id}')],
            [InlineKeyboardButton('Назад', callback_data='del_channel')],
        ]
    )
    return del_channel_markup