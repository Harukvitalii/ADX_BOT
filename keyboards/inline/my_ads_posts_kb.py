from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

ad_post_callback = CallbackData('ad_post_cb', 'increment', 'admin_id')


def my_ads_posts_kb(ad_posts):
    # print(ad_posts)
    btns = InlineKeyboardMarkup(row_width=1)
    if len(ad_posts)!=0:
        ad_btns = [InlineKeyboardButton(ad[6], callback_data=ad_post_callback.new(increment=ad[0],admin_id=ad[1])) for ad in ad_posts]
        print(ad_btns)
        btns.add(*ad_btns)
    btns.add(InlineKeyboardButton('Добавить заготовку', callback_data='add_new_ad_post'))
    btns.add(InlineKeyboardButton('Удалить заготовку', callback_data='del_new_ad_post'))
    btns.add(InlineKeyboardButton('Назад', callback_data='back_to_my_profile'))

    return btns