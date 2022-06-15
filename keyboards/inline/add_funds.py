from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


add_funds = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("BTC banker", callback_data='btc_banker'),
        ]
    ]
)
finances = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Реквизиты", callback_data='requisites'),
        ],
        [ 
            InlineKeyboardButton("Реферальная программа", callback_data='ref_program'),
        ],
        [ 
            InlineKeyboardButton("История операций", callback_data='operation_history'),
        ],
        [InlineKeyboardButton('Вывод', callback_data="withdrow")]
    ]
)


withdrow_funds = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("BTC banker", callback_data='withdrow_btc_banker'),
        ]
    ]
)
