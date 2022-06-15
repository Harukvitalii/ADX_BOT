from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram import types
from loader import dp
from keyboards.inline import help_btns


@dp.message_handler(text = 'Помощь')
async def help_faq(message: Message):
    await message.answer(text='Раздел помощьи', reply_markup=help_btns)
