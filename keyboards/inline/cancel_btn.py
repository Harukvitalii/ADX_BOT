from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cancel_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton(text='Отмена', callback_data='cancel_btn')
        ]
    ]
)

cancel_btn_with_channel_id_faq = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton(text='Как получить', url='https://telegra.ph/Kak-poluchit-id-kanala-01-28')
        ],
        [ 
            InlineKeyboardButton(text='Отмена', callback_data='cancel_btn')
        ]
    ]
)


