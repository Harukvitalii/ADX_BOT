from loader import dp
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


#TO_M
main_menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Просмотр каналов'),
            # KeyboardButton(text='Финансы'), #TO_M
        ],
        [
            KeyboardButton(text='Профиль'),
            KeyboardButton(text='Помощь'),
        ]
    
    
    ], resize_keyboard=True
)