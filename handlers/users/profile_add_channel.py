from aiogram.types.callback_query import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message
from aiogram import types
from keyboards.inline import cancel_btn, cancel_btn_with_channel_id_faq, channel_theme
from loader import dp
from data.config import ADX_POSTER_TOKEN,ADX_POSTER_USERNAME
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from states.channel_in_pg import CHANNEL_IN_DB
import copy,requests,asyncio


@dp.callback_query_handler(text='add_channel',state=None)
async def add_channel(call: CallbackQuery, state: FSMContext):
    await CHANNEL_IN_DB.confirm_manager_bot.set()
    await call.message.edit_text(text='Спасибо что решили добавить свой канал!', 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text="Подробнее",url='https://telegra.ph/Podrobnaya-informaciya-ob-ADX-manager-bot-02-27-2')],
        [InlineKeyboardButton(text="Вперед✊",callback_data='yes_i_added_bot')]]))


    #TO_M 
    # p2p_qiwi_bool = pgbotdb.is_exist_qiwi_p2p_key(call.from_user.id)
    # if p2p_qiwi_bool:
    #     await CHANNEL_IN_DB.confirm_manager_bot.set()
    #     await call.message.edit_text(text='Для начала добавьте нашего бота @ADX_POSTER_bot в свой канал для публикации объявлений', 
    #     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="Подробнее",url='https://telegra.ph/Podrobnaya-informaciya-ob-ADX-manager-bot-02-27-2')],
    #         [InlineKeyboardButton(text="Да, я добавил",callback_data='yes_i_added_bot')]]))
    # else: 
    #     await call.answer('Для начала заполните реквизиты 🦋')


@dp.callback_query_handler(text='yes_i_added_bot',state=CHANNEL_IN_DB.confirm_manager_bot)
async def add_channel(call: CallbackQuery, state: FSMContext):
    await CHANNEL_IN_DB.channel_name.set()
    await call.message.edit_text(text='Введите имя канала ^ ^ ', reply_markup=cancel_btn)
    

@dp.message_handler(state=CHANNEL_IN_DB.channel_name)
async def add_channle_2etap(message: Message, state: FSMContext):
    name = message.text
    async with state.proxy() as channel: 
        channel["name"] = name
    await message.answer(text='Ссылка на канал (с https)', reply_markup=cancel_btn)
    await CHANNEL_IN_DB.next()

@dp.message_handler(state=CHANNEL_IN_DB.channel_link)
async def btc_banker_dep(message: Message, state: FSMContext):
    link = message.text
    if 'join' in link or '+' in link: 
        await message.answer('Мы пока не можем добавлять закрытие канали, в скорем временем исправим!!!')
        await state.finish()
    elif 'https://' not in link: await message.answer('Пожалуйста, отправьте ссылку на канал с https://')
    else:
        async with state.proxy() as channel: 
            channel["link"] = link
            channel['admin_id'] = message.from_user.id
        await message.answer(text='Айти канала', reply_markup=cancel_btn_with_channel_id_faq)
        await CHANNEL_IN_DB.next()



@dp.message_handler(state=CHANNEL_IN_DB.channel_id)
async def btc_banker_dep(message: Message, state: FSMContext):
    id = message.text
    id_try = id
    try: 
        int(id_try)
    except Exception as err: 
        print(err)
        await message.answer(text='Введите число')
        return 0
    async with state.proxy() as channel: 
    #"""TO DO"""  Проверка линка на канал сделать рабочей при запуске рабочей версии
        # TO_M
        # username = check_username(ADX_POSTER_TOKEN, id, channel["link"].replace('https://t.me/',''))
        # if username == 'BOT KICKED OUT': 
        #     await message.answer('Вы удалили нашеге бота @ADX_POSTER_bot с своего канал, добавьте его обратно или вы не сможете добавить канал в ADX')
        #     await state.finish()
        #     return 0
        # elif not username: 
        #     await message.answer('Юзернейм вашего канале не совпадает с тем что вы нам прислали или вы ен добавили бота, проверьте еще раз ^ ^')
        #     await state.finish()
        #     return 0

        channel["id"] = id
    #TO_M проверка есть ли админ мой бот
    # status_adx_poster_admin = check_bot_in_channel_admin(ADX_POSTER_TOKEN,id, ADX_POSTER_USERNAME)
    status_adx_poster_admin = True
    if status_adx_poster_admin == "NO RIGHTS":
        await message.answer(text='Вы добавили бота но у него нет всех нужных прав, убедитесь что бот имеет право слать сообщения и удалять их')
        await state.finish()
        return 0
    elif status_adx_poster_admin:
        await message.answer(text='Введите описание к своему каналу', reply_markup=cancel_btn)
        await CHANNEL_IN_DB.next()
    else: 
        await message.answer(f'Вы не добавили нашего бота в свой канал с айди {id}, исправльте это и начните заново🦋🦋🦋')
        await state.finish()
        return 0


@dp.message_handler(state=CHANNEL_IN_DB.description)
async def btc_banker_dep(message: Message, state: FSMContext):
    description = message.text
    async with state.proxy() as channel: 
        channel["description"] = description
    await message.answer(text='Введите коментарий к своему каналу', reply_markup=cancel_btn)
    await CHANNEL_IN_DB.next()


from keyboards.inline import channel_theme
from loader import themes
@dp.message_handler(state=CHANNEL_IN_DB.comment)
async def btc_banker_dep(message: Message, state: FSMContext):
    comment = message.text
    async with state.proxy() as channel: 
        channel["comment"] = comment
        await message.answer(text='Теперь выберете тематику', reply_markup=channel_theme(themes=copy.deepcopy(themes)))
    await CHANNEL_IN_DB.next()

from keyboards.inline import banned_theme_callback
@dp.callback_query_handler(text_contains='theme', state=CHANNEL_IN_DB.channel_theme)
async def theme(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    #pg db insert theme in channels
    theme = call.data.split(':')[1]
    if theme == '🦋': theme = call.data.split(':')[0]
    async with state.proxy() as channel: 
        channel["theme"] = theme
        channel["banned"] = []
    await call.message.answer('Выберете запрещенные тематики', reply_markup=banned_theme_callback(copy.deepcopy(themes)))
    await call.message.answer('Выберете запрещенные тематики выше')
    await CHANNEL_IN_DB.next()


list_banned = []
@dp.callback_query_handler(text_contains='banned', state=CHANNEL_IN_DB.banned_themes)
async def banned_themes(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as channel: 
        theme_name = call.data.split(":")[1]
        if theme_name not in channel["banned"]:
            channel["banned"].append(theme_name)
        else: channel["banned"].remove(theme_name)
    print(channel["banned"])
    await call.message.edit_text('Выберете запрещенные тематики', reply_markup=banned_theme_callback(copy.deepcopy(themes),channel["banned"]))
    

from keyboards.inline import conditions_prices_kb
from states.channel_in_pg import FSM_CONDITIONS
from loader import pgbotdb
@dp.callback_query_handler(text='baned_next', state=CHANNEL_IN_DB.banned_themes)
async def banned_themes_gotovo(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text= '🦋🦋🦋🦋🦋🦋🦋🦋🦋')
    await call.message.answer(text= 'Теперь введите время постов для своего канала через ",":\nПример:\n11:30, 14:00...')
    await CHANNEL_IN_DB.next()


from keyboards.inline import end_setup_time
@dp.message_handler(state=CHANNEL_IN_DB.time_for_posts)
async def time_for_posts(message: Message, state: FSMContext):
    times = message.text.split(',')
    for time in times:
        time.strip('\n').strip(' ')
        await message.answer(text=time)
    print(times)
    async with state.proxy() as cond:
        cond["times"] = times
    await message.answer(f'Вы можете переотправить если допустили ошибку, или двигаться дальше по кнопке', reply_markup=end_setup_time)


@dp.callback_query_handler(text='end_setup_time', state=CHANNEL_IN_DB.time_for_posts)
async def end_time_for_posts(call: CallbackQuery, state: FSMContext):
    channel_id = ''
    async with state.proxy() as channel:
        pgbotdb.save_channel_info(
        channel_id=channel['id'], 
        admin_id=channel['admin_id'], 
        name=channel['name'], 
        link=channel['link'],
        description=channel['description'], 
        comment=channel['comment'], 
        channels_theme=channel['theme'], 
        banned_themes=json.dumps(channel['banned']),
        times_for_posts=json.dumps(channel['times']))
        channel_id = channel['id']
    await call.message.answer(text= '🦋🦋🦋🦋🦋🦋🦋🦋🦋')
    await call.message.answer(text= 'Введите условия через разделитель ","\n формат как ниже\nв топе/период - цена (без руб)')
#TO_M    # await call.message.answer(text="""Также возможно задать без удаление:\nБессрочно - 999\n⚠️*/24 Обязательно иначе ваш канал будет удален... \nНапример: """)
    await call.message.answer(text="""Также возможно задать без удаление:\nБессрочно - 999\n⚠️*/24 Обязательно для расчета стаимости цени за 1000 просмотров \nНапример: """)
    await call.message.answer(text="""1/24 - 200, 3/48 - 800, Бессрочно - 999""")
    await state.finish()
    await FSM_CONDITIONS.conditions.set()
    async with state.proxy() as channel:
        channel['id'] = channel_id

import json
from keyboards.inline import end_channel_setup
@dp.message_handler(state=FSM_CONDITIONS.conditions)
async def conditions(message: Message, state: FSMContext):
    
    conditions = message.text.split(',')
    cond = []
    print(conditions)
    for condition in conditions:
        condition = condition.split('-')
        condition_time = condition[0].replace(" ", "")
        price = condition[1].replace(" ","")
        await message.answer(f'{condition_time} -  {price} руб')
        cond.append([condition_time, price])
    async with state.proxy() as channel:
        pgbotdb.save_conditions(channel_id=channel['id'],
        conditions = json.dumps(cond))
    #save conditions
        print(condition_time, price)
    await message.answer(f'Вы можете переотправить если допустили ошибку, или завершить ^ ^', reply_markup=end_channel_setup)

    
@dp.callback_query_handler(text='end_channel_setup', state=FSM_CONDITIONS.conditions)
async def end_channel_set(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Вы хорошо поработали 🦋\nВаш канал добавиться в ближайшие 24 часа \nТеперь ваш канал смогут увидеть рекламодатели, изменить данные можно в профиле ^ ^')


# @dp.callback_query_handler(text='con_pr_continue', state=CHANNEL_IN_DB.how_many_dates_of_posts)
# async def banned_themes_gotovo(call: CallbackQuery, state: FSMContext):
#     await call.message.answer(text= '🦋🦋🦋🦋🦋🦋🦋🦋🦋-------------')
#     await call.message.answer(text= 'naic')
#     await CHANNEL_IN_DB.next()



def check_username(bot_api,channel_id,username):
    URL = 'https://api.telegram.org/bot' + bot_api +'/getChat'
    PARAMS = {'chat_id':channel_id}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print(data)
    print('channel_id')
    if data['ok'] == False:
        if data["description"] == "Forbidden: bot was kicked from the channel chat":return 'BOT KICKED OUT'
    try:
        bot_username = data["result"]['username']
    except KeyError: return False
    print(username, bot_username)
    return bool(username == bot_username)


def check_bot_in_channel_admin(bot_api,channel_id,bot_user_id):
    URL = 'https://api.telegram.org/bot' + bot_api +'/getChatMember'
    PARAMS = {'chat_id':channel_id,"user_id":bot_user_id}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print(data)
    if data["result"]["status"] == 'administrator':
        can_post_messages = data['result']["can_post_messages"]
        can_edit_messages = data['result']["can_manage_chat"]
        requirements = (can_edit_messages,can_post_messages)
        print(requirements)
        if all(requirements): return True  
        else: return "NO RIGHTS"
    else: return False