import json
import datetime
import pytz
import os
import random
import string

from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, InputMediaPhoto
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram.utils.exceptions import BadRequest

from keyboards.inline.post_confirmation import post_confirmation_with_kb
from handlers.buy_ads.theme_channel_info_call import condition
from keyboards.inline import post_confirmation
from loader import pgbotdb,dp
from data.config import CLIENT_ID,CLIENT_SECRET
from states.post import POST
from imgurpython import ImgurClient


channel_info_callback = CallbackData('channel_info', 'id', 'page', "sort_by", 'reverse')
Order_callback = CallbackData('order_ads', "id", "condition","time")


# pgbotdb.deploy_post(channel_id=84557, advertiser_id=3498,name='Бойцовский клуб', date_of_post=post_date)

from.theme_channel_info_call import theme_channel_info_callback
@dp.callback_query_handler(text_contains='buy_s_time$')
async def buy_s_time(call: CallbackQuery):
    print(call.data)
    id = call.data.split('$')[1]
    conditions = call.data.split('$')[2]
    channel_times = pgbotdb.select_channel(channel_id=call.data.split('$')[1])[-1]
    channel_times = json.loads(channel_times)
    #сравнить время с уже заказаними рекламами і дать только те что доступние
    # КЛАВИАТУРА ДЛЯ ВИБОРАВ ВРЕМЕНИ ПОСТОВ
    kb = await time_keyboard(channel_times=channel_times,conditions=conditions,id=id,user_id=call.from_user.id)
    #Cмена фото
    await dp.bot.edit_message_media(chat_id=call.from_user.id, message_id=call.message.message_id,
    media=InputMediaPhoto(media='https://i.imgur.com/xge2Ik1.png'))
    #change text
    await dp.bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.message_id,
    caption='Выберите время 🦋-свободно, ❌-занято',
    reply_markup=kb)


@dp.callback_query_handler(text="ignore237482374a",state=None)
async def order_ads_time(call: CallbackQuery,state: FSMContext):
    """Если время занято делаем"""
    await call.answer(text = 'Время уже прошло или занято (')


@dp.callback_query_handler(text_contains=["order_ads$"],state=None)
async def order_ads_time(call: CallbackQuery,state: FSMContext):
    """Отправка поста в после вибора времени"""
    print(call.data)
    cb = call.data.split('$')
    channel_id = cb[1]
    condition =cb[2]
    time = cb[3]
    channel_info = pgbotdb.select_channel(channel_id)
    admin_id = channel_info[2]
    channel_link = channel_info[4]
    identifier = get_random_string(8)
    #TO_M
    # await call.message.edit_media(media=InputMediaPhoto('https://i.imgur.com/iI95wyg.png'))
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Назад',callback_data='choose_what_to_do_from_all_channels')]])
    # await call.message.edit_caption(caption='Отправльте пост в HTML формате',reply_markup=kb)
    # await POST.post.set()
    # async with state.proxy() as post:
    #     post['channel_id']  = channel_id 
    #     post['condition'] =  condition
    #     post['time'] = time 
    chan_cond = pgbotdb.get_conditions(channel_id)
        # post['post_price'] =  post_price
    post_price = [c_cond[1] for c_cond in chan_cond \
                              if c_cond[0]== condition]
    print('channel_id', channel_id, 'condition', condition, 'time', time, 'post price',post_price)
    await call.message.answer(
    text=f"""<code>@ADX_INC_bot order:{identifier}</code>
Вот ваша ссылка, можете отправить админу <a href='tg://user?id={admin_id}'>🦋Admin🦋</a> """,reply_markup=kb,parse_mode='HTML')
    pgbotdb.add_order_link_for_admin(identifier, channel_id,channel_link,condition, post_price[0],time)




@dp.message_handler(state=POST.post,content_types=["photo", "text"])#,content_types=['photo', 'text']
async def order_ads_time(message: Message,state:FSMContext):
    """Принимаем пост и возвращаем его"""
    text = ''
    file_id = int
    if message.media_group_id != None:
        return await dp.bot.send_message(message.from_user.id,'Поддержка 2+ фото, видео будет в ближайшее вреия ^ ^')
    else:
        try:
            file_id = message.photo[-1].file_id
            text = message.caption
            await message.photo[-1].download(f'adx_graph/template/post_images/post_image_{message.photo[-1].file_id[1:7]}.png')
            image_dir = f'adx_graph/template/post_images/post_image_{message.photo[-1].file_id[1:7]}.png'
            img_link = save_img_imgur(image_dir)
            print(img_link)
            os.remove(image_dir) 
            image_dir = ''
        except IndexError:
            img_link = 0
            text = message.text
    async with state.proxy() as post:
        post['ordered_by_id']= message.from_user.id
        post['text']= text
        post['pictue_id'] = img_link #file_id
        post['parse_mode']= 'HTML'
        post['time_in_channel']= post['time'] 
        if post['condition'] == 'Бессрочно':
            post['end_of_post'] = datetime.datetime.now(pytz.timezone('Europe/Moscow')) + datetime.timedelta(days=30000)
            print(post['time'])
            print(post['end_of_post'])
        else:
            add_hours = post['condition'].split('/')[1]
            post_date = datetime.datetime.strptime(post['time'], '%Y-%m-%d %H:%M:%S')
            end_date = post_date + datetime.timedelta(hours=int(add_hours))
            print(post_date)
            print(end_date)
            post['end_of_post'] = end_date 
        post['confirmed']= 'False' #TO DO Сменить на False при випуске приложухи

        if img_link == 0:
            try:
                await dp.bot.send_message(chat_id=message.from_user.id, text=text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
            reply_markup=post_confirmation)
            except CantParseEntities:
                await dp.bot.send_message(chat_id=message.from_user.id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
        else:
            # await dp.bot.send_media_group(chat_id=ADMIN, media=mg)
            # await dp.bot.send_media_group(chat_id=ADMIN,media=message.media_group_id)
            try:
                await dp.bot.send_photo(message.from_user.id, file_id, text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
            reply_markup=post_confirmation)
            except TypeError: 
                await dp.bot.send_message(chat_id=message.from_user.id, text="" + '\n\n⚠ Пост не может быть без текста ^ ^')
            except CantParseEntities:
                await dp.bot.send_message(chat_id=message.from_user.id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
        

# медиа груп
# @dp.message_handler(state=POST.post,content_types=[ContentType.DOCUMENT, ContentType.TEXT])#,content_types=['photo', 'text']
# async def order_ads_time(message: Message,state:FSMContext):
#     if message.media_group_id != None:
#         return await dp.bot.send_message(message.from_user.id,'Поддержка 2+ фото, видео будет в ближайшее вреия ^ ^')


@dp.callback_query_handler(state=POST.post,text="add_button_to_post")
async def post_conf(call: CallbackQuery, state: FSMContext):
    """Добавить кнопку"""
    print("Адд Биттон")
    await call.message.answer('Пожалуйсва введите текст и ссылку.\nтекст = url, разделитель "," как в примере. \nПример: \nADX = https://t.me/adx_inc_bot, ADX CHAT = https://t.me/adx_community\n\n⚠️Если вы не хотите добавлять кнопки, пришлите "-"')
    await POST.kb.set()


@dp.message_handler(state=POST.kb)
async def get_kb_for_post(mg:Message, state: FSMContext):
    photo_true = True
    async with state.proxy() as post: 
        if post['pictue_id'] == 0:
            photo_true = False
        if mg.text == '-' or mg.text == '"-"':
            post['kb'] == '-'
            if not photo_true:
                post_kb = await send_post_without_photo(chat_id=mg.from_user.id,text=post['text'])
            else:
                post_kb = await send_post_with_photo(chat_id=mg.from_user.id,picture_id=post['pictue_id'], text=post['text'])
        else: 
            if not photo_true:
                post_kb = await send_post_without_photo(chat_id=mg.from_user.id,text=post['text'],kb=mg.text)
            else:
                post_kb = await send_post_with_photo(chat_id=mg.from_user.id,picture_id=post['pictue_id'], text=post['text'],kb=mg.text)
        post['kb'] = json.dumps(post_kb)
    await POST.post.set()



@dp.callback_query_handler(state=POST.post,text="post_confirmation")
async def post_conf(call: CallbackQuery, state: FSMContext):
    """Подтверждение поста"""
    print("OKEEEEEEY")
    # async with state.proxy() as post:
        # post['channel_id']
        # post['ordered_by_id']
        # post['text']
        # post['pictue_id'] 
        # post['parse_mode']
        # post['post_price']#1/24
        # post['time_in_channel']
        # post['end_of_post']
        # post['confirmed']
    await call.message.delete()
    await call.message.answer('Ваш пост добавлен, осталось лишь оплатить 🦋',
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton('Qiwi/Карта', callback_data='qiwi_pay')],[InlineKeyboardButton('Отмена', callback_data='cancel_btn')]]))
#оплата


def callback_time_for_posts(add_days:int, channel_times: list,conditions,id,posts):
    """СОЗДАЕТ ЛИСТ С ВРЕМЕНЕМ ДЛЯ ТЕКСТА И ДАТОЙ ПОСТА ДЛЯ КОЛБЕКА"""
    available = '🦋'
    not_available = '❌'
    btns = []
    date_now = datetime.datetime.now(pytz.timezone('Europe/Moscow')).date()
    if add_days != 0:date_now = date_now + datetime.timedelta(days=add_days)
    for time in channel_times:
        not_available_date = ''
        date_format = str(date_now) +' '+ time + ":00"
        post_date = datetime.datetime.strptime(date_format,'%Y-%m-%d %H:%M:%S')
        for post in posts:
            if int(post[1]) == int(id) and post[7]==post_date:
                not_available_date = post_date
        if not_available_date != '':
            btns.append(InlineKeyboardButton(text=time+not_available, callback_data=f'ignore237482374a'))   #'ignore237482374a'
        elif post_date+datetime.timedelta(minutes=15)<=datetime.datetime.now():
            btns.append(InlineKeyboardButton(text=time+not_available, callback_data=f'ignore237482374a'))   #'ignore237482374a'
        else:
            btns.append(InlineKeyboardButton(text=time+available, callback_data=f'order_ads${id}${conditions}${post_date}'))
    
    return btns



async def time_keyboard(channel_times, conditions, id, user_id):
    posts = pgbotdb.get_posts()
    kb = InlineKeyboardMarkup(row_width=3)
    kb.row(InlineKeyboardButton(text='Сегодня', callback_data='948397530'))
    btns1 = callback_time_for_posts(add_days=0, channel_times=channel_times, conditions = conditions,id=id,posts=posts)
    print(btns1)
    # btns1 =(InlineKeyboardButton(text=time, callback_data=f'order_ads${id}${conditions}${date}') for time,date in cb_today)
    kb.add(*btns1)
    kb.row(InlineKeyboardButton(text='Завтра', callback_data='ignore'))
    btns2 = callback_time_for_posts(add_days=1, channel_times=channel_times, conditions = conditions,id=id,posts=posts)
    kb.add(*btns2)
    kb.row(InlineKeyboardButton(text='Послезавтра', callback_data='ignore'))
    btns3 = callback_time_for_posts(add_days=2, channel_times=channel_times, conditions = conditions,id=id,posts=posts)
    kb.add(*btns3)
    cb_info = pgbotdb.select_user_back_from_times(user_id=user_id)
    print('cb_infoooooooooooooooooooooooooooooooooo')
    print(cb_info)
    if cb_info[6] == '-':
        kb.row(InlineKeyboardButton('Назад', callback_data=channel_info_callback.new(cb_info[1+1], cb_info[2+1], cb_info[3+1], cb_info[4+1])))
    else: kb.row(InlineKeyboardButton('Назад', callback_data=theme_channel_info_callback.new(cb_info[1+1], cb_info[2+1], cb_info[3+1], cb_info[4+1], cb_info[5+1])))
    return kb



def save_img_imgur(file_dir,client_id = CLIENT_ID,client_secret = CLIENT_SECRET):
    client = ImgurClient(client_id, client_secret)
    r = client.upload_from_path(file_dir, config=None, anon=True)
    return r['link']


async def send_post_without_photo(chat_id,text, kb='-',rm=post_confirmation):
    if kb!='-':
        post_kb = kb.split(',')
        kb = post_kb
        rm = post_confirmation_with_kb(post_kb)
    try:
        await dp.bot.send_message(chat_id=chat_id, text=text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
    reply_markup=rm)
    except CantParseEntities:
        await dp.bot.send_message(chat_id=chat_id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
    except BadRequest: 
        await dp.bot.send_message(chat_id=chat_id, text="" + '\n\n⚠ Ссылка из кнопки не валидна, попробуйте еще раз^ ^')
    return kb
    

async def send_post_with_photo(chat_id,picture_id, text, kb='-',rm=post_confirmation):
    if kb!='-':
        kb = kb.split(',')
        rm = post_confirmation_with_kb(kb)
    try:
        await dp.bot.send_photo(chat_id, picture_id, text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
    reply_markup=rm)
    except TypeError: 
        await dp.bot.send_message(chat_id=chat_id, text="" + '\n\n⚠ Пост не может быть без текста ^ ^')
    except CantParseEntities:
        await dp.bot.send_message(chat_id=chat_id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
    except BadRequest: 
        await dp.bot.send_message(chat_id=chat_id, text="" + '\n\n⚠ Ссылка из кнопки не валидна, попробуйте еще раз^ ^')
    return kb

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str