
from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import Message, message
from states.fsm_payments import FSMPAYWM
from loader import dp


@dp.message_handler(text = 'Webmoney', state=None)
async def qiwi(message: Message):
    await message.answer(text='В розработке...')
    # await FSMPAY.wm.set()
    # await dp.bot.delete_message(call.from_user.id, call.message.message_id)
    # await dp.bot.send_message(chat_id=call.from_user.id, text='Введите сумму пополнения ниже: ')

@dp.message_handler(state=FSMPAYWM.wm)
async def get_value(message: Message, state = FSMPAYWM):
    async with state.proxy() as data:
        data['deposit'] = message.text
        dep = data['deposit']
        await message.reply(text = f'{dep} in WebMoney')
    await state.finish()

@dp.message_handler(text = 'Yoomoney', state=None)
async def qiwi(message: Message):
    await message.answer(text='В розработке...')