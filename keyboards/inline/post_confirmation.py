from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




post_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Добавить кнопку", callback_data='add_button_to_post')
        ],
        [ 
            InlineKeyboardButton("Подтвердить", callback_data='post_confirmation')
        ],
        [ 
            InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels')
        ],
    ]
)


post_confirmation_add_ads = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("Добавить кнопку", callback_data='add_button_to_post')
        ],
        [ 
            InlineKeyboardButton("Подтвердить", callback_data='add_ads_post_to_db')
        ],
        [ 
            InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels')
        ],
    ]
)




def post_confirmation_with_kb(kb, row_width=1):
    "TO DO" # сделать уязвимость до букв, сделать только числа для row_width
    split_error = False
    keb = InlineKeyboardMarkup(row_width=row_width)
    data = []
    for kb_text_url in kb: 
        try:
            text = kb_text_url.split('=')[0]
            url = kb_text_url.split('=')[1]
        except IndexError:
            split_error = True
        data.append([text.replace(' ', ''),url.replace(' ', '')])
    if split_error:
        keb.add(InlineKeyboardButton("Неверный разделитель :(", callback_data='post_confirmation'))
        keb.add(InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels'))
    else:
        btns = (InlineKeyboardButton(text = text,url=url) for text,url in data)
        keb.add(*btns)
        keb.add(InlineKeyboardButton("Подтвердить", callback_data='post_confirmation'))
        keb.add(InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels'))
    print(data)
    return keb


def post_confirmation_with_kb_add_ads_post(kb, row_width=1):
    "TO DO" # сделать уязвимость до букв, сделать только числа для row_width
    split_error = False
    keb = InlineKeyboardMarkup(row_width=row_width)
    data = []
    for kb_text_url in kb: 
        try:
            text = kb_text_url.split('=')[0]
            url = kb_text_url.split('=')[1]
        except IndexError:
            split_error = True
        data.append([text.replace(' ', ''),url.replace(' ', '')])
    if split_error:
        keb.add(InlineKeyboardButton("Неверный разделитель :(", callback_data='add_ads_post_to_db'))
        keb.add(InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels'))
    else:
        btns = (InlineKeyboardButton(text = text,url=url) for text,url in data)
        keb.add(*btns)
        keb.add(InlineKeyboardButton("Подтвердить", callback_data='add_ads_post_to_db'))
        keb.add(InlineKeyboardButton("Назад", callback_data='choose_what_to_do_from_all_channels'))
    print(data)
    return keb


