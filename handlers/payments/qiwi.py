
# from aiogram import types
# from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
# from utils.misc.check_if_not_adx_pay import check_if_not_adx_pay
# from aiogram.types.callback_query import CallbackQuery
# from aiogram.utils.callback_data import CallbackData
# from aiogram.dispatcher.storage import FSMContext
# from aiogram.types import Message, message
# from data.config import ADMIN, QIWI_BILL_DELL, QIWI_P2P_TOKEN
# from states.fsm_payments import FSMPAYQIWI
# from states.post import POST
# from pyqiwip2p import QiwiP2P
# from loader import dp, pgbotdb 
# from random import randint
# import datetime as dt
# import asyncio,pytz
# qiwi_pay_callback = CallbackData('qiwi_pay', 'bill')


# def buy_qiwi_menu(isUrl=True, url='', bill=''):
#     qiwi_pay = InlineKeyboardMarkup(row_width=1)
#     if isUrl:
#         pay_btn = InlineKeyboardButton(text = 'Оплатить', url=url)
#         qiwi_pay.add(pay_btn)
#     qiwi_check = InlineKeyboardButton(text = 'Проверить оплату', callback_data=qiwi_pay_callback.new(bill))
#     qiwi_pay.add(qiwi_check)
#     qiwi_pay.add(InlineKeyboardButton('Отмена', callback_data='cancel_btn'))
#     return qiwi_pay

# def is_number(_str):
#     try:
#         int(_str)
#         return True
#     except ValueError:
#         return False


# @dp.callback_query_handler(text ='qiwi_pay', state=POST.post)
# async def qiwi(call:CallbackQuery, state: FSMContext):
#     """Сохранение поста после нажатие на кнопку оплатить"""
#     async with state.proxy() as post:
#         # post['channel_id']
#         # post['ordered_by_id']
#         # post['text']
#         # post['pictue_id'] 
#         # post['parse_mode']
#         # post['post_price']
#         # post['time_in_channel']
#         # post['end_of_post']
#         # post['confirmed']
#         #post['kb']
#         channel = pgbotdb.select_channel(post['channel_id'])
#         print(channel)
#         channel_cpv = pgbotdb.select_channel_statistic_today(post['channel_id'])[-1]
#         #qiwi bill
#         QIWI_P2P_ADMIN_TOKEN = pgbotdb.get_p2p_qiwi_token(channel[2])
#         time_to_earn = check_if_not_adx_pay(post['channel_id'], ADMIN)
#         if time_to_earn: 
#             QIWI_P2P_ADMIN_TOKEN = QIWI_P2P_TOKEN # токен админа
#             post['ordered_by_id'] = ADMIN # меняем ордеред бай на админовский
#         p2p = QiwiP2P(auth_key=QIWI_P2P_ADMIN_TOKEN, currency = 'RUB')
#         try:
#             bill = p2p.bill(
#                 amount=int(post['post_price']), 
#                 lifetime=QIWI_BILL_DELL,
#                 comment=str(post['ordered_by_id']) + str(post['channel_id']))
#         except ValueError:
#             await qiwi_token_error(
#                 channel_id = post['channel_id'], 
#                 ordered_by = post['ordered_by_id'])
#                 #заменяем ключ на свой и создаем новий бил
#             p2p = QiwiP2P(auth_key=QIWI_P2P_TOKEN, currency = 'RUB')
#             bill = p2p.bill(
#                 amount=int(post['post_price']), 
#                 lifetime=QIWI_BILL_DELL,
#                 comment=str(post['ordered_by_id']) + str(post['channel_id']))
#         # except Exception as err: print("err ", err)
#         try:
#             pgbotdb.save_post_from_user(
#             post['channel_id'], 
#             post['ordered_by_id'],
#             post['text'], 
#             post['pictue_id'], 
#             post['parse_mode'], 
#             post['time_in_channel'], 
#             post['end_of_post'], 
#             post['confirmed'],
#             bill.bill_id,post['post_price'],
#             kb=post['kb'])
#         except KeyError as err:
#             print(err)
#             pgbotdb.save_post_from_user(
#             post['channel_id'], 
#             post['ordered_by_id'],
#             post['text'], 
#             post['pictue_id'], 
#             post['parse_mode'], 
#             post['time_in_channel'], 
#             post['end_of_post'], 
#             post['confirmed'],
#             bill.bill_id,post['post_price'],
#             kb="-")
#         pgbotdb.create_qiwi_bill(
#             QIWI_P2P_TOKEN,
#             call.message.from_user.id, 
#             int(post['post_price']), 
#             bill.bill_id, 
#             created_date=dt.datetime.now(pytz.timezone("Europe/Moscow")))

#         await call.message.edit_text(text=f"""Цена поста в канале <a href='{channel[4]}'>{channel[3]}</a>
# Дата начала публикации: {str(post['time_in_channel'])}
# Дата окончания: {str(post['end_of_post'])}
# Цена: {post['post_price']}руб
# Цена за 1000 просмотров: ~ {channel_cpv}руб
# Заказчик: {call.from_user.first_name}

# 🦋🦋🦋
# Команда @adx_inc_bot
# """,reply_markup=buy_qiwi_menu(url=bill.pay_url,bill=bill.bill_id), disable_web_page_preview=True)
#     await state.finish()
#     await FSMPAYQIWI.qiwi.set()
#     async with state.proxy() as qiwi:
#         qiwi['p2p'] = p2p

# @dp.callback_query_handler(qiwi_pay_callback.filter(), state=FSMPAYQIWI.qiwi)#state=FSMPAYQIWI.deposit
# async def check(call: CallbackQuery, callback_data: dict, state:FSMContext):  #state: FSMContext
#     print(callback_data)
#     bill_id = callback_data['bill']
#     # print(bill_id)
#     bill_exists, bill_info = pgbotdb.is_exists_qiwi_bill(bill_id)
#     if bill_exists != False:
#         p2p = ''
#         async with state.proxy() as qiwi:
#             p2p = qiwi['p2p']
#         if str(p2p.check(bill_id=bill_id).status) == 'PAID': #DONE
#             deposit = bill_info[3]
#             await dp.bot.send_message(
#                 chat_id=ADMIN, 
#                 text=f'Рекламу оплачено на сумму {deposit} RUB, Юзером @{call.from_user.username} ID:{call.from_user.id}')
#             await dp.bot.send_message(
#                 chat_id=call.from_user.id, 
#                 text=f'Рекламу оплачено на сумму {deposit} RUB')
#             pgbotdb.confirm_post_payment(bill_id = bill_info[4]) 
#             pgbotdb.add_balance_to_spent_on_ads(call.from_user.id,deposit) #update spent balance
#             await inform_admin_ads(bill_id=bill_info[4],spent=deposit) #уведомления админу что у него купили рекламу
            
#         else:
#             await dp.bot.send_message(chat_id=call.from_user.id, text='Вы не оплатили счет, проверьте статус', reply_markup=buy_qiwi_menu(False,bill=bill_id))
#     else:
#         pass
#         await dp.bot.send_message(chat_id=call.from_user.id, text='Счет не найден')
#     await state.finish()



# async def inform_admin_ads(bill_id,spent):
#     post_info = pgbotdb.get_post_by_bill_id(bill_id)
#     channel_info = pgbotdb.select_channel(post_info[1])
#     admin_id = channel_info[2]
#     pgbotdb.add_balance_to_earned(admin_id,spent) #добавим на баланс админа денег
#     text = f"""🦋У вас новая завка на рекламу в канале <a href='{channel_info[4]}'>{channel_info[3]}</a>
# Время {post_info[7]}
# Цена: {post_info[6]}
# Текст поста:
# {post_info[3]}"""
#     await dp.bot.send_message(admin_id, text, disable_web_page_preview=True)


# async def qiwi_token_error(channel_id, ordered_by):
#     channel_info = pgbotdb.select_channel(channel_id)
#     admin_id = channel_info[2]
#     await dp.bot.send_message(admin_id, 'Ваш киви токен не рабочий, пожалуства исправьте эту проблему, покупатели не могут купить у вас рекламу, пока не будет исправлен токен мы будет принимать платежи на свой киви. \nP.S ADX TEAM')
#     await dp.bot.send_message(ADMIN, f'⚠️⚠️⚠️Ключ киви <a href="tg://user?id={admin_id}">Админа</a>, не работает')
#     # await dp.bot.send_message(ordered_by, f'Ключ киви <a href="tg://user?id={admin_id}">Админа</a>, не работает, мы уже сообщили ему об этом, сейчас вы можете оплатить рекламу на наши реквизиты выше')




















