from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def conditions_prices_kb(cond_pr: dict, check_btns=None):

    if check_btns != None:
        for banned in check_btns:
            cond_pr[banned] = '🦋'
        for k,v in cond_pr.items():
            if v == '🦋' and k not in check_btns:
                cond_pr[k] = k
    kb = InlineKeyboardMarkup(row_width=2)
    btns = (InlineKeyboardButton(text=v, callback_data=f'conditions_{k}') for k,v in cond_pr.items())
    kb.add(*btns)
    kb.row(InlineKeyboardButton(text='Продолжить', callback_data='con_pr_continue'))
    return kb


end_channel_setup = InlineKeyboardMarkup( 
    inline_keyboard=[ 
        [InlineKeyboardButton('Завершить', callback_data="end_channel_setup")]
    ]
)






