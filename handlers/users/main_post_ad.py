from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from aiogram import types
from loader import dp
from keyboards.inline import post_ad_kb
from states.add_ad_post_state import AD_POST

@dp.message_handler(text='Просмотр каналов')
async def post_ad(message: Message):
    await message.answer('Выберите что будем делать дальше ^ ^', reply_markup=post_ad_kb)


@dp.callback_query_handler(text='choose_what_to_do_from_all_channels')
async def post_ad(call:CallbackQuery, state: FSMContext):
    await state.finish()
    await dp.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Выберите что будем делать дальше ^ ^', reply_markup=post_ad_kb)


from states.post import POST
@dp.callback_query_handler(text='choose_what_to_do_from_all_channels',state=[POST.post])
async def post_ad(call:CallbackQuery, state: FSMContext):
    await state.finish()
    await dp.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Выберите что будем делать дальше ^ ^', reply_markup=post_ad_kb)