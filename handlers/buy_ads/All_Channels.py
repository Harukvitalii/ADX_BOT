from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, InputMediaPhoto
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import pgbotdb,dp
from .all_channel_info import channel_info_callback

sort_channels_callback = CallbackData('all_channels', 'act', 'page', "sort_by", 'reverse')

class ALL_CANNELS:
    
    async def all_chann_kb(
        self,
        channel_statistics: list,
        reverse: str = "False",
        page: int = 1,
        sort_by: str = "ERR",
        channels_inone_page: int = 5,
    ):  
        up = '▲'
        down = '▼'
        pdp_icon = ''
        err_icon = ''
        cpv_icon = ''
        if sort_by =='ПДП':
            pdp_icon = down if reverse=='False' else up
        else: pdp_icon=''
        if sort_by =='CPV':
            cpv_icon = down if reverse=='False' else up
        else: cpv_icon=''
        if sort_by =='ERR':
            err_icon = down if reverse=='False' else up
        else: err_icon=''


        kb = InlineKeyboardMarkup(row_width=1)
        
        btns = [
            InlineKeyboardButton(text='ПДП'+ pdp_icon, callback_data=sort_channels_callback.new('SORT', 1, "ПДП",reverse)),
            InlineKeyboardButton(text='ERR'+ err_icon, callback_data=sort_channels_callback.new('SORT', 1, "ERR",reverse)),
            InlineKeyboardButton(text='CPV'+ cpv_icon, callback_data=sort_channels_callback.new('SORT', 1, "CPV",reverse))
            ]
        kb.row(*btns)
        page, btn_list = get_list_of_channels(channel_statistics,channels_inone_page, page)
        
        # берем по статистике ERR канали, отбираем первый 10 x штук и добавляем в клаву
        chn_btns = (InlineKeyboardButton(text=f'{round(channel[2],2)}руб {round(100*channel[1],1)}% {channel[4]} {channel[3]}', 
        callback_data=channel_info_callback.new(channel[0], page, sort_by, reverse)) for channel in btn_list)
        
        kb.add(*chn_btns)
        if page != 1:
            kb.row(InlineKeyboardButton(text='<<<', callback_data=sort_channels_callback.new("GO_BACK",page,sort_by,reverse)),
        InlineKeyboardButton(text='^  ^', callback_data=sort_channels_callback.new('OPEN_UP', page, sort_by,reverse)),
        InlineKeyboardButton(text='>>>', callback_data=sort_channels_callback.new("GO_FORTH",page,sort_by,reverse)),)
        elif page == 1: kb.row(InlineKeyboardButton(text='Назад', callback_data='choose_what_to_do_from_all_channels'),
        InlineKeyboardButton(text='^  ^', callback_data=sort_channels_callback.new('OPEN_UP', page, sort_by,reverse)),
        InlineKeyboardButton(text='>>>', callback_data=sort_channels_callback.new("GO_FORTH",page,sort_by,reverse)),)
        return kb



    async def process_selection(self, call: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates new kb for channels
        """
        statistics = pgbotdb.select_all_channel_statistics_today()

        if data['act'] == "SORT":
            sort_by = data['sort_by']
            if sort_by == "ERR":
                
                try:
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics=sorted(statistics, key=lambda err: err[10]),sort_by='ERR'))
                except MessageNotModified: 
                    print("Сообщение не изменено")
                    print("reverse = true")
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics=sorted(statistics, key=lambda err: err[10], reverse=True),sort_by='ERR',reverse=True))
            
            elif sort_by == "CPV":

                try:
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics=sorted(statistics, key=lambda cpv: cpv[11]),sort_by='CPV'))
                except MessageNotModified: 
                    print("Сообщение не изменено")
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics=sorted(statistics, key=lambda cpv: cpv[11], reverse=True),sort_by='CPV',reverse=True))
            
            elif sort_by == "ПДП":
                try:
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics=sorted(statistics, key=lambda sub: sub[3]),sort_by="ПДП"))
                except MessageNotModified: 
                    print("Сообщение не изменено")
                    await call.message.edit_reply_markup(await self.all_chann_kb(
                        channel_statistics= sorted(statistics, key=lambda err: err[10], reverse=True),sort_by="ПДП",reverse=True))
            
        # user picked a day button, return date
        if data['act'] == "GO_FORTH":
            """DONE""" # Чтобі после последней страници ишла первая $Сделано
            rev = data['reverse']
            print("in go forth",rev)
            sort_by = data['sort_by']
            sorted_list = []
            if sort_by == "ERR":
                sorted_list = sorted(statistics, key=lambda err: err[10])
            elif sort_by == "CPV":
                sorted_list = sorted(statistics, key=lambda cpv: cpv[11])
            elif sort_by == "ПДП":
                sorted_list = sorted(statistics, key=lambda sub: sub[3])
            
            if rev=='True':
                sorted_list.reverse()
            await call.message.edit_reply_markup(await self.all_chann_kb(
            channel_statistics=sorted_list,
            sort_by = data['sort_by'],
            page = int(data['page'])+1,
            reverse=rev
            ))
            

        if data['act'] == "GO_BACK":
            sort_by = data['sort_by']
            sorted_list = []
            page = int(data['page'])-1
            if page<=0:
                page = 1
            if sort_by == "ERR":
                sorted_list = sorted(statistics, key=lambda err: err[10])
            elif sort_by == "CPV":
                sorted_list = sorted(statistics, key=lambda cpv: cpv[11])
            elif sort_by == "ПДП":
                sorted_list = sorted(statistics, key=lambda sub: sub[3])
            if data['reverse'] == 'True':
                sorted_list.reverse()
            await call.message.edit_reply_markup(await self.all_chann_kb(
            channel_statistics=sorted_list,
            sort_by = data['sort_by'],
            page = page,
            reverse=data['reverse']))

        if data['act'] == 'IGNORE':
            await call.answer(cache_time=60)
        if data['act'] =='BACK':
            sorted_list = []
            rev = data['reverse']
            sort_by = data['sort_by']
            if sort_by == "ERR":
                sorted_list = sorted(statistics, key=lambda err: err[10])
            elif sort_by == "CPV":
                sorted_list = sorted(statistics, key=lambda cpv: cpv[11])
            elif sort_by == "ПДП":
                sorted_list = sorted(statistics, key=lambda sub: sub[3])
            if rev=='True':
                sorted_list.reverse()
            print('ALL CHANNEL')
            await dp.bot.edit_message_media(media=InputMediaPhoto(media='https://i.ibb.co/cX95b6c/adx-banner.png'), chat_id=call.from_user.id, message_id=call.message.message_id)
            await call.message.edit_caption(caption ='1-средняя цена за 1000 просмотров, 2-ERR, Тема, Название канала', reply_markup=await self.all_chann_kb(
            channel_statistics=sorted_list,
            sort_by = data['sort_by'],
            page = int(data['page']),
            reverse=data['reverse']
            ))

    





def get_list_of_channels(channel_statistics,channels_inone_page, page):
    btn_list = []
    count = 0
    for channel in channel_statistics:
        btn_one = []
        btn_one.append(channel[1]) #channel_id
        btn_one.append(channel[10]) #err
        btn_one.append(channel[11]) #cpv
        btn_one.append(pgbotdb.select_channel(channel_id=channel[1])[3]) #name
        btn_one.append(pgbotdb.select_channel(channel_id=channel[1])[7]) #theme
        btn_list.append(btn_one)


    delete_elements = (page-1)*channels_inone_page
    if page==1:
        result = []
        for btn in btn_list:
            result.append(btn)
            count+=1
            if count == channels_inone_page:
                break
    else:
        result = []
        for btn in btn_list:
            if delete_elements > 0:
                delete_elements-=1 
            else:
                result.append(btn)
                count+=1
                if count == channels_inone_page:
                    break
    
    if len(result)==0:
        btn_list = get_list_of_channels(channel_statistics,channels_inone_page,1)
        return "1", btn_list[1]
        
    return page, result
