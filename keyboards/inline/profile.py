import aiogram
from loader import pgbotdb

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


profile_menu_callback = CallbackData('profile_menu', "act")






def profile_kb_text(user_id):
    opposite_role = 'Реламодателем' if pgbotdb.user_is_admin(user_id) else 'Админом'

    user_info = pgbotdb.user_info(user_id=user_id)
    first_name = user_info[1]
    username = user_info[2]
    user_balance = user_info[6]
    spent_on_ad = user_info[7]
    earned = user_info[8]

    profile_text_admin = f"""-📱 Ваш профиль {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Вы:  Админ 
🦋 Логин: @{username}
🦋 ID: {user_id}
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋"""
    
    text = f"""-📱 Ваш профиль {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Вы: Рекламодатель
🦋 Логин: @{username}
🦋 ID: {user_id}
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋"""
#

    profile_kb = InlineKeyboardMarkup(row_width=1)
    ad_stats = InlineKeyboardButton(text = 'Cтатистика рекл.', callback_data=profile_menu_callback.new('Cтатистика рекл.')),
    my_channels = InlineKeyboardButton('Мои канали', callback_data="my_channels")
    
    my_ad_posts = InlineKeyboardButton('Мои рекл. пости', callback_data="my_ads_posts")
    change_role = InlineKeyboardButton('Стать '+opposite_role, callback_data='change_role')
    
    
    withdrow = InlineKeyboardButton('Вывод', callback_data="withdrow")
    posts_in_progres = InlineKeyboardButton('Заявки в прогрессе', callback_data='zajavka_in_progress')
    
    if pgbotdb.is_exists_admin(user_id):
        # profile_kb.add(ad_stats)
        profile_kb.add(my_channels)
        profile_kb.add(my_ad_posts)
        profile_kb.add(change_role)
        # profile_kb.add(posts_in_progres)
        # profile_kb.add(withdrow)
        text = profile_text_admin
    else: 
        profile_kb.add(change_role)
    return profile_kb, text








