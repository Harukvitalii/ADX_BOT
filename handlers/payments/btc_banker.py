
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import Message, message
from data.config import ADMIN
from states.fsm_payments import FSMBTC_BANKER
from loader import dp, pgbotdb
from keyboards.inline import cancel_btn

def is_number(number):
    try:
        int(number)
        return True
    except: return False


@dp.callback_query_handler(text="btc_banker", state=None)
async def btc_banker(call: CallbackQuery, state: FSMContext):
    await FSMBTC_BANKER.btc_banker.set()
    await call.message.answer(text='Введите сумму пополнения: ', reply_markup=cancel_btn)
    await FSMBTC_BANKER.next()


@dp.message_handler(state=FSMBTC_BANKER.check)
async def btc_banker_dep(message: Message, state: FSMContext):
    dep = message.text
    dep_bool = is_number(dep)
    print(dep_bool)
    if dep_bool:
        await message.answer(text='Теперь отправльте чек: ', reply_markup=cancel_btn)
        await FSMBTC_BANKER.next()


# @dp.message_handler(state=FSMBTC_BANKER.check)
# async def btc_banker_check(message: Message):
#     btc_check = message.text
#     #обнал чека 
