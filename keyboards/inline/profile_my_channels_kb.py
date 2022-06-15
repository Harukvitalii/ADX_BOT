
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



profile_my_channels_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Настройка существующих", callback_data='change_channel_settings')
        ],
        [ 
            InlineKeyboardButton("Добавить", callback_data='add_channel')
        ],
        [ 
            InlineKeyboardButton("Удалить", callback_data='del_channel')
        ],
    ]
)