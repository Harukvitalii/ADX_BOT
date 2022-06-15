from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram import types
from loader import dp
from keyboards.default.main_menu import main_menu


@dp.message_handler(text = 'Отмена')
async def cancel_dep(message: Message):
    await message.answer(text='Меню', reply_markup=main_menu)



@dp.callback_query_handler(state='*')
@dp.callback_query_handler(text = 'cancel_btn', state='*')
async def cancel_state(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    # print(current_state)
    if current_state is None:
        return
    await state.finish()
    await call.message.answer('Отменено', reply_markup=main_menu)