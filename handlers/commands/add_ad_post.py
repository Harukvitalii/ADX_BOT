import os
import json
import json
import asyncio

from imgurpython import ImgurClient
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram.utils.exceptions import BadRequest

from data.config import CLIENT_ID, CLIENT_SECRET
from keyboards.inline.post_confirmation import post_confirmation_with_kb_add_ads_post
from keyboards.inline import post_confirmation_add_ads
from states.add_ad_post_state import AD_POST
from loader import pgbotdb,dp




@dp.message_handler(state=AD_POST.name,content_types=["photo", "text"])#,content_types=['photo', 'text']
async def order_ads_time(message: Message,state:FSMContext):
    async with state.proxy() as post: 
        post['name'] = message.text
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Отмена',callback_data='calncel_btn')]])
    await message.answer_photo(photo='https://i.imgur.com/iI95wyg.png',caption='Отправльте пост в HTML формате',reply_markup=kb)
    await AD_POST.post.set()


@dp.message_handler(state=AD_POST.post,content_types=["photo", "text"])#,content_types=['photo', 'text']
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
        post['admin_id']= message.from_user.id
        post['text']= text
        post['pictue_id'] = img_link #file_id
        post['parse_mode']= 'HTML'
        if img_link == 0:
            try:
                await dp.bot.send_message(chat_id=message.from_user.id, text=text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
            reply_markup=post_confirmation_add_ads)
            except CantParseEntities:
                await dp.bot.send_message(chat_id=message.from_user.id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
        else:
            # await dp.bot.send_media_group(chat_id=ADMIN, media=mg)
            # await dp.bot.send_media_group(chat_id=ADMIN,media=message.media_group_id)
            try:
                await dp.bot.send_photo(message.from_user.id, file_id, text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
            reply_markup=post_confirmation_add_ads)
            except TypeError: 
                await dp.bot.send_message(chat_id=message.from_user.id, text="" + '\n\n⚠ Пост не может быть без текста ^ ^')
            except CantParseEntities:
                await dp.bot.send_message(chat_id=message.from_user.id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
    

@dp.callback_query_handler(state=AD_POST.post,text='add_ads_post_to_db')#,content_types=['photo', 'text']
async def order_ads_time(call: CallbackQuery,state:FSMContext):
    "Всі збережені данні після додавання поста"
    await asyncio.sleep(0.5)
    await dp.bot.delete_message(call.from_user.id,call.message.message_id)
    async with state.proxy() as post:
        admin_id = post['admin_id']
        text = post['text']
        pictue_id = post['pictue_id']
        parse_mode = post['parse_mode']
        name = post['name']
        try: kb = post['kb']
        except: kb = post['kb'] = '-'
        print(post['pictue_id'],post['admin_id'],post['kb'],post['parse_mode'],post['text'])
        pgbotdb.save_ads_post_for_admin(admin_id,text,pictue_id,parse_mode,kb,name)
    await call.message.answer('Ваше обьявление добавлено в базу данных 🦋')
    await state.finish()


@dp.callback_query_handler(state=AD_POST.post,text="add_button_to_post")
async def post_conf(call: CallbackQuery, state: FSMContext):
    """Добавить кнопку"""
    print("Адд Биттон")
    await call.message.answer('Пожалуйсва введите текст и ссылку.\nтекст = url, разделитель "," как в примере. \nПример: \n<code>ADX = https://t.me/adx_inc_bot, ADX CHAT = https://t.me/adx_community</code>\n\n⚠️Если вы не хотите добавлять кнопки, пришлите "-"')
    await AD_POST.kb.set()


@dp.message_handler(state=AD_POST.kb)
async def get_kb_for_post(mg:Message, state: FSMContext):
    """Додавання клаватури і відправка поста обратно"""
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
    await AD_POST.post.set()



def save_img_imgur(file_dir) -> str:
    """Вигрзка файла на imgur"""
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    client = ImgurClient(client_id, client_secret)
    r = client.upload_from_path(file_dir, config=None, anon=True)
    print(r['link'])
    return r['link']



async def send_post_without_photo(chat_id,text, kb='-',rm=post_confirmation_add_ads):
    if kb!='-':
        post_kb = kb.split(',')
        kb = post_kb
        rm = post_confirmation_with_kb_add_ads_post(post_kb)
    try:
        await dp.bot.send_message(chat_id=chat_id, text=text + '\n\n⚠ Вы можете переотправить пост, если допустили ошибку или продолжить ^ ^',
    reply_markup=rm)
    except CantParseEntities:
        await dp.bot.send_message(chat_id=chat_id, text='\n\n⚠В вашем тексте есть не верный тег проверьте попробуйте пожалуйста еще раз ^ ^\n Можете слать сразу после этого текста')
    except BadRequest: 
        await dp.bot.send_message(chat_id=chat_id, text="" + '\n\n⚠ Ссылка из кнопки не валидна, попробуйте еще раз^ ^')
    return kb
    

async def send_post_with_photo(chat_id,picture_id, text, kb='-',rm=post_confirmation_add_ads):
    if kb!='-':
        kb = kb.split(',')
        rm = post_confirmation_with_kb_add_ads_post(kb)
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