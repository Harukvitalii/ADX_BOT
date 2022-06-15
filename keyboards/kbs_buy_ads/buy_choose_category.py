from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import pgbotdb

def buy_choose_category(call_prefix: str):
    
    channels_info = pgbotdb.get_all_channels()
    themes = []
    for theme in channels_info:
        themes.append(theme[7])
    res = []
    [res.append(x) for x in themes if x not in res]
    themes = res
    print(themes)
    buy_choose_category  =  InlineKeyboardMarkup(row_width=2)

    btns = [
        InlineKeyboardButton(text='Пдп', callback_data=call_prefix + ':sort_by_pdp'),
        InlineKeyboardButton(text='ERR', callback_data=call_prefix + ':sort_by_err'),
        InlineKeyboardButton(text='CPV', callback_data=call_prefix + ':sort_by_spv')
        ]

    # buy_choose_category.row(*btns)
    theme_btns = (InlineKeyboardButton(text=theme, callback_data=call_prefix + ':' + theme) for theme in themes)
    
    buy_choose_category.add(*theme_btns)
    buy_choose_category.row(InlineKeyboardButton(text="Назад", callback_data="choose_what_to_do_from_all_channels"))
    return buy_choose_category




