from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_role = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Админ", callback_data='user_is_admin'),
            InlineKeyboardButton('Рекламодатель',callback_data='user_is_adveriser'),
        ]
    ]
)