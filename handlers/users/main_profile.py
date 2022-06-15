from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram import types
from loader import dp,pgbotdb
from keyboards.default.main_menu import main_menu
from keyboards.inline import profile_kb_text
from states.add_ad_post_state import AD_POST
from states.fsmqiwi_reqv import QIWI_P2P_REQV

@dp.message_handler(text='Профиль')
async def profile(message: Message):
    kb, text = profile_kb_text(message.from_user.id)
    await message.answer(text=text, reply_markup=kb)


@dp.callback_query_handler(text='back_to_my_profile')
async def profile(call: CallbackQuery):
    kb, text = profile_kb_text(call.from_user.id)
    await call.message.edit_text(text=text, reply_markup=kb)

@dp.callback_query_handler(text='back_to_my_profile',state=[QIWI_P2P_REQV.token,AD_POST.name])
async def profile(call: CallbackQuery, state:FSMContext):
    await state.finish()
    kb, text = profile_kb_text(call.from_user.id)
    await call.message.edit_text(text=text, reply_markup=kb)
    #список из инлайн кнопок имен каналов


from keyboards. inline import withdrow_funds
@dp.callback_query_handler(text='withdrow')
async def withdrow(call: CallbackQuery):
    if True: await call.answer('Будет доступно после внедрения реф программи')
    else:
        user_info = pgbotdb.user_info(call.from_user.id)
        await call.message.answer(f'👑 Баланс: {user_info[6]} RUB',reply_markup=withdrow_funds)

@dp.callback_query_handler(text='withdrow_btc_banker')
async def withdrow_btc_banker(call: CallbackQuery):
    await call.message.answer('Введите суму вывода')






from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


kb_req = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton("QIWI", callback_data='qiwi_reqv'),],    
        [ 
            InlineKeyboardButton("BTC banker", callback_data='btc_banker_reqv'),
        ],
        [ 
            InlineKeyboardButton("WEBMONEY", callback_data='wm_reqv'),],   
        [ 
            InlineKeyboardButton("Назад", callback_data='back_to_my_finances'),],   
    ]
)


@dp.callback_query_handler(text='requisites')
async def requisites(call:CallbackQuery):
    await call.message.edit_text(text='Выберите систему платежей для настройки', reply_markup=kb_req)

 #qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi
@dp.callback_query_handler(text='qiwi_reqv',state=None)
async def qiwi_reqv(call:CallbackQuery, state: FSMContext):
    await QIWI_P2P_REQV.token.set()
    qiwi_p2p_bool = pgbotdb.is_exist_qiwi_p2p_key(user_id = call.from_user.id)
    print(qiwi_p2p_bool)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Более подробная информация", url='https://telegra.ph/ADX-Informaciya-o-QIWI-P2P-model-02-20'))
    kb.add(InlineKeyboardButton("Назад", callback_data="back_to_my_finances"))
    kb.add(InlineKeyboardButton("Отмена", callback_data="cancel_btn"))
    if qiwi_p2p_bool:
        token = pgbotdb.get_p2p_qiwi_token(call.from_user.id)
        await call.message.edit_text(text=f"У вас уже есть P2P ключ\n Ваш ключ: {token}\n, но вы можете вветсти его заново", reply_markup=kb)
    else:
        await call.message.edit_text(text="Введите P2P ключ для проверки платежей", reply_markup=kb)
    async with state.proxy() as kb_s:
        kb_s['kb'] = kb

@dp.message_handler(state=QIWI_P2P_REQV.token)
async def qiwi_reqvstate(mg: Message, state: FSMContext):
     async with state.proxy() as kb_s:
        kb=kb_s['kb']
        kb_s['token'] = mg.text
        kb.add(InlineKeyboardButton("Подтвердить", callback_data='confirm_p2pqiwi'))
        await mg.answer(text=f"Ваш P2P ключ будет: {mg.text}\n⚠️ Проверьте правильность, иначе вы не сможете принимать платежи", reply_markup=kb)


@dp.callback_query_handler(text='confirm_p2pqiwi',state=QIWI_P2P_REQV.token)
async def qiwi_reqv_call_confirm(call:CallbackQuery, state: FSMContext):
    async with state.proxy() as qiwi:
        pgbotdb.save_p2p_qiwi_token(user_id=call.from_user.id, token=qiwi['token'])
    await call.message.answer('Ваш токен обновлен. Спасибо что вы с нами 🦋')
    await state.finish()
# qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwi qiwiv qiwi qiwi qiwi qiwi qiwi qiwi qiwi 


"""TO DO""" 
@dp.callback_query_handler(text='btc_banker_reqv')
async def btc_banker_reqv(call:CallbackQuery):
    await call.answer(text='Скоро...')


"""TO DO"""
@dp.callback_query_handler(text='wm_reqv')
async def wm_reqv(call:CallbackQuery):
    await call.answer(text='Скоро...')



"""DONE"""
@dp.callback_query_handler(text='ref_program')
async def wm_reqv(call:CallbackQuery):
    await call.answer(text='Реферальная программа')
    await call.message.answer('\n100руб за привлеченного Aдмина\n 65руб за привлеченного Рекламодателя\nВаша реферальная ссылка: \n<code>https://t.me/adx_inc_bot?start={}</code>'.format(call.from_user.id))



"""TO DO"""
@dp.callback_query_handler(text='operation_history')
async def wm_reqv(call:CallbackQuery):
    await call.answer(text='Скоро история операций...')