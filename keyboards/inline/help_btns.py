from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

help_btns = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("FAQ", url='https://telegra.ph/FAQ-ADX-INC-01-27'),],
        [InlineKeyboardButton('Админ',url='t.me/adx_admin'),],
        [InlineKeyboardButton('Помощник',url='t.me/vetallb'),],
    ]
)