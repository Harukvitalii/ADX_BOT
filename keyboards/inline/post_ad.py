from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

post_ad_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Выбрать категорию", callback_data='choose_category')
        ],
        [ 
            InlineKeyboardButton("Смотреть все канали", callback_data='choose_all_channels')
        ],
    ]
)