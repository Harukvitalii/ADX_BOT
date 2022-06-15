from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram import types
from loader import dp,pgbotdb
from keyboards.inline import add_funds,finances
from aiogram.dispatcher.storage import FSMContext


#TO_M

#TO_DO psycopg2.InterfaceError: cursor already closed

@dp.message_handler(text = 'Финансы')
async def help_faq(message: Message):
    user_info = pgbotdb.user_info(user_id=message.from_user.id)
    first_name = user_info[1]
    user_balance = user_info[6]
    spent_on_ad = user_info[7]
    earned = user_info[8]
    ref_balance = user_info[9]
    finance_text_admin = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Продано рекл. на сумму: {earned} RUB
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    finance_text = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    if pgbotdb.is_exists_admin(message.from_user.id):
        finance_text = finance_text_admin
    await message.answer(text=finance_text, reply_markup=finances)



@dp.callback_query_handler(text='back_to_my_finances')
async def help_faq(call: CallbackQuery):
    user_info = pgbotdb.user_info(user_id=call.from_user.id)
    first_name = user_info[1]
    user_balance = user_info[6]
    spent_on_ad = user_info[7]
    earned = user_info[8]
    ref_balance = user_info[9]
    finance_text_admin = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Продано рекл. на сумму: {earned} RUB
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    finance_text = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    if pgbotdb.is_exists_admin(call.from_user.id):
        finance_text = finance_text_admin
    await call.message.edit_text(text=finance_text, reply_markup=finances)

from states.fsmqiwi_reqv import QIWI_P2P_REQV
@dp.callback_query_handler(text='back_to_my_finances',state=QIWI_P2P_REQV.token)
async def help_faq(call: CallbackQuery,state:FSMContext):
    await state.finish()
    user_info = pgbotdb.user_info(user_id=call.from_user.id)
    first_name = user_info[1]
    user_balance = user_info[6]
    spent_on_ad = user_info[7]
    earned = user_info[8]
    ref_balance = user_info[9]
    finance_text_admin = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Продано рекл. на сумму: {earned} RUB
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    finance_text = f"""-👛 Финансы {first_name}:
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
🦋 Потрачено на рекламу: {spent_on_ad} RUB
🦋 Реф. баланс: {ref_balance} RUB
🦋 Баланс: {user_balance} RUB
🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋
"""
    if pgbotdb.is_exists_admin(call.from_user.id):
        finance_text = finance_text_admin
    await call.message.edit_text(text=finance_text, reply_markup=finances)

