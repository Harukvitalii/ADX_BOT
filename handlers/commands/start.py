import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline import choose_role
from keyboards.default import main_menu
from loader import dp, pgbotdb
from data.config import ADMIN
import datetime,pytz
# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await dp.bot.send_message(message.from_user.id,text='Menu', reply_markup=main_menu)




@dp.message_handler(CommandStart())
async def show_menu(message: types.Message):

    print(message.text)

    user_bool = pgbotdb.is_exists_user(message.from_user.id)
    if not user_bool: #doesnt' exist in db
        await message.answer(text = f'Добро пожаловать в ADX {message.from_user.first_name}')
        await asyncio.sleep(1)
        date_enter = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d')
        pgbotdb.register_user(message.from_user.first_name, message.from_user.username, message.from_user.id, date_enter, 0, 0, 0, 0)
        pgbotdb.insert_user_back_from_times(message.from_user.id,0,0,'ERR','True')
        await dp.bot.send_message(chat_id=ADMIN, text=f'🦋Зарегистрирован новый пользователь @{message.from_user.username}, id: {message.from_user.id}')

    admin_bool = pgbotdb.is_exists_admin(message.from_user.id)
    if admin_bool: await message.answer(text = 'Спасибо что выбрали нас ^ ^', reply_markup=main_menu) 
    else: await message.answer(text = 'Выберете кем вы являетесь: ', reply_markup=choose_role)

    if 'reserve' in message.text: 
        print(message.text)
        return 0 

    if ' ' in message.text: 
        ref = message.text.split()[1]
        print(ref,message.from_user.id)
        if str(ref) == str(message.from_user.id): await message.answer('Вы не можете быть сами себе рефералом🦋')
        else: 
            if pgbotdb.register_referral(ref,message.from_user.id) == 'UniqueViolation':
                await message.answer('Вы не можете быть рефералом двох человек или одного и тоже человека дважди\nПропишите /start')


@dp.callback_query_handler(text='user_is_admin')
async def i_am_admin(call: types.CallbackQuery):
    pgbotdb.set_user_admin(call.from_user.id)
    await call.message.answer(text = "Спасибо за ваш выбор", reply_markup=main_menu)


@dp.callback_query_handler(text='user_is_adveriser')
async def user_is_adveriser(call: types.CallbackQuery):
    pgbotdb.user_is_adveriser(call.from_user.id)
    await call.message.answer(text = "Спасибо за ваш выбор", reply_markup=main_menu)



#Рефферал
# @dp.message_handler(commands=["start"])
# async def referral(message: types.Message):
#     print(message.text)