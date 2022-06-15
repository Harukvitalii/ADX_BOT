

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



end_setup_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Далее", callback_data='end_setup_time')
        ],
        [ 
            InlineKeyboardButton("Отмена", callback_data='cancel_btn')
        ],

    ]
)

end_setup_time_change = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Далее", callback_data='end_setup_time_change')
        ],
        [ 
            InlineKeyboardButton("Отмена", callback_data='cancel_btn')
        ],

    ]
)