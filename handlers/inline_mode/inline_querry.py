import hashlib
import json
import datetime
from random import randint


from loader import bot,dp,pgbotdb
from aiogram.types import InlineQuery, InlineQueryResultPhoto, \
    InputTextMessageContent, InlineQueryResultArticle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery




@dp.inline_handler()
async def inline_handler(query: InlineQuery):
    switch_text = "Перейти в бота можно нажав на это сообщение"
    channel_statistics= pgbotdb.select_all_channel_statistics_today()
    channel_infos = pgbotdb.get_all_channels()
    channel_images = pgbotdb.get_channel_stat_img(1,True)
    admin_posts_imgs = pgbotdb.select_ads_post_for_admin(query['from'].id)
    admin_posts_text = pgbotdb.select_ads_post_for_admin(query['from'].id,imgs=False)

    print(query.query)
    if 'post' in query.query or 'пости' in query.query:
        # if len(admin_posts) != 0:
        posts = []
        print("пости")
        for post in admin_posts_imgs:
            p = InlineQueryResultPhoto(
                id=post[0],
                title = 'Пост',
                description=f"Постик",
                photo_url = post[3],
                thumb_url = post[3],
                caption=post[2], #text
                reply_markup=post_kb(json.loads(post[5])), #kb
                parse_mode="HTML"
                ) if post[5] != '-' else \
                InlineQueryResultPhoto(
                id=post[0],
                title = 'Пост',
                description=f"Постик",
                photo_url = post[3],
                thumb_url = post[3],
                caption=post[2], #text
                parse_mode="HTML"
                )
            posts.append(p)
        await query.answer(
            posts, cache_time=60, is_personal=True,
            switch_pm_parameter="add", switch_pm_text=switch_text)
    elif 'text' in query.query or 'текст' in query.query:
        posts = []
        print("пости")
        for post in admin_posts_text:
            
            p = InlineQueryResultArticle(
                id=post[0],
                title = post[6],
                description=post[2][0:75],
                input_message_content=InputTextMessageContent(
                message_text = post[2],
                disable_web_page_preview=True),
                reply_markup=post_kb(json.loads(post[5])), #kb
                ) if post[5] != '-' else \
                InlineQueryResultArticle(
                id=post[0],
                title = post[6],
                description=post[2][0:75],
                input_message_content=InputTextMessageContent(
                message_text = post[2],
                disable_web_page_preview=True),
                )
            posts.append(p)
        await query.answer(
            posts, cache_time=60, is_personal=True,
            switch_pm_parameter="add", switch_pm_text=switch_text)
    
    elif 'order:' in query.query:
        indentifier = query.query.replace('order:','')
        order_info = pgbotdb.select_order_link_for_admin(indentifier)
        channel_name = pgbotdb.select_channel(order_info[2])[3]
        imgs = [img for img in channel_images if img[1]==order_info[2]][0]
        time = order_info[6]
        logo_img = imgs[3]
        order = [InlineQueryResultArticle(
                id=indentifier,
                title=f"{order_info[4]} - {order_info[5]}₽ реклама в канале: {channel_name}",
                description=f"Заявка на рекламу {str(time)}",
                hide_url=True,
                thumb_url = logo_img,
                input_message_content=InputTextMessageContent(
                message_text = f"""Здравствуйте. Хочу заказать у вас рекламу в канале <a href="{order_info[3]}">🦋{channel_name}🦋</a>
Дата: {time.strftime('%Y-%m-%d')}
Время: {time.strftime('%H:%M:%S')}
Условия: {order_info[4]} 
Цена: {order_info[5]}₽
Как можно оплатить?""",
                parse_mode="HTML",
                disable_web_page_preview=True),
                #TO_DO Сделать чтоби при переходе в бота можно було б зарезервировать место
                # reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                #     [InlineKeyboardButton('Reserve (For ADMIN)❗',url=f't.me/adx_inc_bot/start=reserve{order_info[2]}')] #:{str(time).replace(" ","-")}
                #     ])
            )]
        await query.answer(
            order, cache_time=300, is_personal=False,switch_pm_parameter="add", switch_pm_text=switch_text)

    else:
        articles = []
        for channel_stat in channel_statistics:
            channel_info = [ch_info for ch_info in channel_infos if ch_info[1]==channel_stat[1]][0]
            if query.query not in channel_info[3]: continue
            imgs = [img for img in channel_images if img[1]==channel_stat[1]][0]
            stats_img = imgs[2]
            logo_img = imgs[3]
            print(imgs)
            forbidden_themes = forbid_theme(json.loads(channel_info[8]))
            channel_conditions = pgbotdb.get_conditions(channel_stat[1])
            article = InlineQueryResultArticle(
                id=channel_stat[0],
                title=channel_info[3],
                description=f"Тематика: {channel_info[7]}\nSubs: {format_number_to_k(channel_stat[3])}  ERR: {channel_stat[10]*100:.2f}%  CPV: {channel_stat[-1]}₽ за 1000👀",
                url=stats_img,
                hide_url=True,
                thumb_url = logo_img,
                input_message_content=InputTextMessageContent(
                    message_text=f"<a href='{stats_img}'> </a>" + f"""Ссылка на канал: 🦋 <a href='{channel_info[4]}'>{channel_info[3]}</a> 🦋
Запрещенные тематики: {forbidden_themes}
Тематика: {channel_info[7]}
Подписчиков: {channel_stat[3]} чел. 
Условия: {' '.join(map(condition, channel_conditions))}
Цена за 1000 views: ~{channel_stat[-1]} руб
Комментарий: {channel_info[6]}

❗ <a href='tg://user?id={channel_info[2]}'>Админ канала</a> ❗"""[0:1023],
                    parse_mode="HTML", #Описание: \n{channel_info[5]}\n
                ),
                
                # reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton('❗ Админ ❗',url=f)]])
            )
            articles.append(article)
        await query.answer(articles, cache_time=60, is_personal=False,
                            switch_pm_parameter="add", switch_pm_text=switch_text)


@dp.callback_query_handler(text='reserve_channel')
async def reserve_channel(call: CallbackQuery):
    print(call.from_user.id)




def forbid_theme(theme:list):
    string = ''
    if len(theme) == 0:
        return 'Нет'
    for i in theme:
        string = string + i
    return string

def condition(cond :list)->str:
    string = '\n' + str(cond[0]) + ' - ' + str(cond[1]) + ' руб'
    return string


def format_number_to_k(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def post_kb(kb):
    """Работа с клавиатурой"""
    keb = InlineKeyboardMarkup(row_width=1)
    print(kb)
    if '=' in kb[0]:
        btns = (InlineKeyboardButton(text=k.split('=')[0].strip(' '), url=k.split('=')[1].strip(' ')) for k in kb)
    else:
        btns = (InlineKeyboardButton(text=text, url=url) for text,url in kb)
    keb.add(*btns)
    print(keb)
    return keb
