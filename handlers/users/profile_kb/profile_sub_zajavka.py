import json
import asyncio

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData


from keyboards.inline.profile import profile_menu_callback
from keyboards.inline import profile_my_channels_kb, my_ads_posts_kb
from keyboards.inline.my_ads_posts_kb import ad_post_callback
from states.add_ad_post_state import AD_POST
from loader import dp,pgbotdb



admin_post_stats_callback = CallbackData('admin_kb', "act", 'user_id', 'page')
post_statistics_callback = CallbackData('post_stats', "act", 'user_id', 'page', 'reverse')


@dp.callback_query_handler(profile_menu_callback.filter())
async def statistics_ad(call: CallbackQuery):
    # pass
    # posts = pgbotdb.get_posts()
    text, kb = await POST_STATS().post_statistics_kb(call.from_user.id,0)
    if text== "no data": await call.answer("У вас еще нет Статистики рекламы")
    else: await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)


@dp.callback_query_handler(post_statistics_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    await POST_STATS().process_selection(call, callback_data)


@dp.callback_query_handler(text='my_channels')
async def my_channels(call: CallbackQuery):
    await call.message.edit_text(text='🦋Мои канали🦋', reply_markup=profile_my_channels_kb)


@dp.callback_query_handler(text='my_ads_posts')
async def my_ads_posts(call: CallbackQuery):
    """Назад до Мои рекл. пости"""
    ad_posts = pgbotdb.select_ads_post_for_admin(call.from_user.id,imgs='ALL')
    await call.message.edit_text("Ваши пости для рекламы/Добавить заготовку", reply_markup=my_ads_posts_kb(ad_posts))

@dp.callback_query_handler(text='my_ads_posts',state=[AD_POST.name])
async def my_ads_posts(call: CallbackQuery,state: FSMContext):
    """Назад до Мои рекл. пости FSM"""
    await state.finish()
    ad_posts = pgbotdb.select_ads_post_for_admin(call.from_user.id, imgs='ALL')
    await call.message.edit_text("Ваши пости для рекламы/Добавить заготовку", reply_markup=my_ads_posts_kb(ad_posts))



@dp.callback_query_handler(text='add_new_ad_post')
async def my_ads_posts(call: CallbackQuery):
    """Добавить новый пост в базу"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Назад',callback_data='back_to_my_profile')]])
    await call.message.edit_text(text="Введите имя для этого поста, в будущем с помощью него можно будеть найты этот пост среди других", reply_markup=kb)
    await AD_POST.name.set()


@dp.callback_query_handler(text='del_new_ad_post')
async def my_ads_posts(call: CallbackQuery):
    """kb при удалении пост из бази"""
    ad_posts = pgbotdb.select_ads_post_for_admin(admin_id=call.from_user.id, imgs='ALL')
    kb = InlineKeyboardMarkup(row_width=1)
    kb_posts = [InlineKeyboardButton(text=adpost[6], callback_data='del_ad_post:'+str(adpost[0])) for adpost in ad_posts]
    kb.add(*kb_posts)
    kb.add(InlineKeyboardButton('Назад',callback_data='back_to_my_profile'))
    await call.message.edit_text(text="Выберите заготовку для удаления", reply_markup=kb)


@dp.callback_query_handler(text_contains='del_ad_post')
async def my_ads_posts(call: CallbackQuery):
    """Удалить пост из бази"""
    
    id_post = call.data.replace('del_ad_post:', '')
    pgbotdb.delete_ads_post_for_admin_by_id(post_id=id_post)
    await call.message.answer('Успешно удалено ✅')


@dp.callback_query_handler(ad_post_callback.filter())
async def ad_post_callback(call: CallbackQuery, callback_data: dict):
    """Отправка поста юзеру"""
    post_info = pgbotdb.select_ad_post_from_db_where_increment(callback_data['increment'])
    print('here')
    await send_post(call.from_user.id,post_info[2],post_info[5],post_info[3])
    await asyncio.sleep(1)
    kb = InlineKeyboardMarkup(row_width=1, 
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data='my_ads_posts')]
            ])
    await call.message.answer(
        text='Назад к постам', 
        reply_markup=kb)


@dp.callback_query_handler(text='change_role')
async def my_channels(call: CallbackQuery):
    role = 'Рекламодатель' if pgbotdb.user_is_admin(call.from_user.id) else 'Админ'
    if pgbotdb.user_is_admin(call.from_user.id): 
        pgbotdb.upadte_user_role(call.from_user.id,role='advertiser')
    else: pgbotdb.upadte_user_role(call.from_user.id,role='admin')
    print('new_role', role)
    await call.answer(f'Вы сменили свою роль на {role}')


@dp.callback_query_handler(text='zajavka_in_progress')
async def posts_in_progres(call: CallbackQuery):
    print("progess")
    text, kb = await ADMIN_ADS().post_kb(call.from_user.id,0)
    if text== "no data": await call.answer("У вас еще нет Заявок на рекламу в ваших каналу (ах)")
    else: await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)


@dp.callback_query_handler(admin_post_stats_callback.filter())
async def choose_category(call: CallbackQuery, callback_data: dict):
    await ADMIN_ADS().kb_logic_change(call, callback_data)


async def send_post(channel_id,text,kb,file_id)->str: 
    """Отправка поста"""
    msg = ''
    if file_id == '0':
        if kb=='-':
            msg = await dp.bot.send_message(chat_id=channel_id, text=text)
        else: 
            msg = await dp.bot.send_message(chat_id=channel_id, text=text,reply_markup=post_kb(json.loads(kb)))
        return msg
    else: 
        if kb=='-':
            msg = await dp.bot.send_photo(channel_id, file_id, text)
        else: 
            msg = await dp.bot.send_photo(channel_id, file_id, text,reply_markup=post_kb(json.loads(kb)))
        return msg


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




class ADMIN_ADS:
    
    async def post_kb(
        self,
        user_id,
        page:int=0,
        reverse: str = "False",
    ) -> ReplyKeyboardMarkup:  
        up = '▲'
        down = '▼'
        stat_icon = down if reverse=='False' else up
        kb=InlineKeyboardMarkup(row_width=1)
        btns = [
            InlineKeyboardButton(text='По дате'+ stat_icon, callback_data=admin_post_stats_callback.new("SORT",user_id, 1)),
            ]
        kb.row(*btns)
        page, info_text = get_post_info_admin(user_id,page)
        if page=='no data':
            return page, ''
        # info_text = "OST_INFO"

        # берем по статистике ERR канали, отбираем первый 10 x штук и добавляем в клаву
        
        if page != 0:
            kb.row(InlineKeyboardButton(text='<<<', callback_data=admin_post_stats_callback.new("GO_BACK",user_id, page)),
        InlineKeyboardButton(text='^  ^', callback_data=admin_post_stats_callback.new('OPEN_UP', user_id, page)),
        InlineKeyboardButton(text='>>>', callback_data=admin_post_stats_callback.new("GO_FORTH",user_id, page)),)
        elif page == 0: kb.row(InlineKeyboardButton(text='Назад', callback_data='back_to_my_profile'),
        InlineKeyboardButton(text='^  ^', callback_data=admin_post_stats_callback.new('OPEN_UP', user_id, page)),
        InlineKeyboardButton(text='>>>', callback_data=admin_post_stats_callback.new("GO_FORTH",user_id, page)),)
        return info_text, kb



    async def kb_logic_change(self, call: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates new kb for channels
        """
        print('IN PORCESSING')

        # user picked a day button, return date
        if data['act'] == "GO_FORTH":
            
            page = data["page"]
            user_id = data["user_id"]

            text, kb = await self.post_kb(user_id,int(page)+1)
            await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)
            

        if data['act'] == "GO_BACK":
            
            page = data["page"]
            user_id = data["user_id"]

            text, kb = await self.post_kb(call.from_user.id,int(page)-1)
            await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)

        if data['act'] == "SORT":
            await call.answer('Будет скоро...')

        if data['act'] == 'IGNORE':
            await call.answer(cache_time=60)
        


class POST_STATS:
    
    async def post_statistics_kb(
        self,
        user_id,
        page:int=0,
        reverse: str = "False",
    ):  
        up = '▲'
        down = '▼'
        stat_icon = down if reverse=='False' else up
        kb=InlineKeyboardMarkup(row_width=1)
        btns = [
            InlineKeyboardButton(text='По дате'+ stat_icon, callback_data=post_statistics_callback.new("SORT",user_id, 1, reverse)),
            ]
        kb.row(*btns)
        page, info_text = get_post_info(user_id,page,reverse)
        if page=='no data':
            return page, ''
        # info_text = "OST_INFO"

        # берем по статистике ERR канали, отбираем первый 10 x штук и добавляем в клаву
        
        if page != 0:
            kb.row(InlineKeyboardButton(text='<<<', callback_data=post_statistics_callback.new("GO_BACK",user_id, page,reverse)),
        InlineKeyboardButton(text='^  ^', callback_data=post_statistics_callback.new('OPEN_UP', user_id, page,reverse)),
        InlineKeyboardButton(text='>>>', callback_data=post_statistics_callback.new("GO_FORTH",user_id, page,reverse)),)
        elif page == 0: kb.row(InlineKeyboardButton(text='Назад', callback_data='back_to_my_profile'),
        InlineKeyboardButton(text='^  ^', callback_data=post_statistics_callback.new('OPEN_UP', user_id, page,reverse)),
        InlineKeyboardButton(text='>>>', callback_data=post_statistics_callback.new("GO_FORTH",user_id, page,reverse)),)
        return info_text, kb



    async def process_selection(self, call: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates new kb for channels
        """
        print('IN PORCESSING')

        # user picked a day button, return date
        if data['act'] == "GO_FORTH":
            rev = data['reverse']
            page = data["page"]
            user_id = data["user_id"]

            text, kb = await self.post_statistics_kb(user_id,int(page)+1, rev)
            await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)

            # if rev=='True':
            #     sorted_list.reverse()
            # await call.message.edit_reply_markup(await self.post_statistics_kb(
            # channel_statistics=sorted_list,
            # sort_by = data['sort_by'],
            # page = int(data['page'])+1,
            # reverse=rev
            # ))
            

        if data['act'] == "GO_BACK":
            rev = data['reverse']
            page = data["page"]
            user_id = data["user_id"]

            text, kb = await POST_STATS().post_statistics_kb(call.from_user.id,int(page)-1, rev)
            await call.message.edit_text(text, reply_markup=kb, disable_web_page_preview=True)

        """TO DO""" # сортировка по дате
        if data['act'] == "SORT":
            await call.answer('Будет скоро...')

        if data['act'] == 'IGNORE':
            await call.answer(cache_time=60)
        



from handlers.payments.btc_banker import is_number
def get_post_info(user_id,page,reverse):
    page, post_info = pgbotdb.posts_ads_statistics(user_id,page)
    if page=='no data':
        return page, ''
    print(post_info)
    status = post_info[10]
    msg_id = post_info[11]
    chan_id = post_info[1]
    print(page, 'pageeeeeeeeeeeeeee')
    views_count='-'

    if status == 'False'or status == False:
        cpv = 'Вы не оплатили пост, у вас есть максимум 5 минут чтобы это сделать!'
    elif status == 'PAID':
        cpv = 'Дождытесь окончание поста'
    elif status == 'SUSPANDED':
        cpv = 'Бот постер был удален админом или канал заблокирован, пишите @ad_manager, решим проблему'
    elif status == 'UNKNOWN':
        cpv = 'Незвестрая ошибка, пишите админу, исправим!!! @adx_admin @adx_manager'
    elif status == 'SENT':
        cpv = 'Пост отправлен в канал, просмотри идут'
    elif status == 'DONE':
        views_count = pgbotdb.posts_stats_views(msg_id,chan_id) 
        try:
            cpv = post_info[6]/views_count*1000 if is_number(views_count) else 'Дождытесь окончание поста'
        except ZeroDivisionError: cpv = "∞"
    chann_info = pgbotdb.select_channel(chan_id)
    text=f"""Реклама в канале <a href='{chann_info[4]}'>{chann_info[3]}</a>
Дата публикации: {post_info[7]}
Дата завершения: {post_info[8]}
по МСК
Количество просмотров: {views_count}
Цена: {post_info[6]}
CPV(Цена за 1к просм.): {cpv}
Статус: {status}
"""
    return page, text



def get_post_info_admin(user_id,page):
    admin_channels = pgbotdb.select_channels(user_id)
    channels= []
    for i in admin_channels:
        channels.append(i)
    page, post_info = pgbotdb.posts_admin_ads_statistics(channels,page)
    if page=='no data':
        return page, ''
    msg_id = post_info[-2]
    chan_id = post_info[1]
    
    views_count = "Пост в процессе публикации" if msg_id == None or msg_id == '-' else pgbotdb.posts_stats_views(msg_id,chan_id)
    chann_info = pgbotdb.select_channel(chan_id)

    cpv = post_info[6]/views_count*1000 if is_number(views_count) else 'Дождытесь окончание поста'
    text=f"""Реклама в вашем канале <a href='{chann_info[4]}'>{chann_info[3]}</a>
Дата публикации: {post_info[7]}
Дата завершения: {post_info[8]}
по МСК
Количество просмотров: {views_count}
Получено: {post_info[6]}
CPV(Цена за 1к просм.): {cpv}
"""
    return page, text







