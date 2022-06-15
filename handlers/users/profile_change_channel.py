import json
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram import types
from keyboards.inline import cancel_btn, cancel_btn_with_channel_id_faq, end_channel_setup
from keyboards.inline import my_channels,change_channel_parameters,change_channel_row,back_to_channel_rows
from loader import dp, pgbotdb
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
import asyncio,copy
from keyboards.inline.callback_data import my_channels_callback
from states.change_channel import CHANGE_ID, CHANGE_banned,CHANGE_comment,CHANGE_description,CHANGE_LINK,CHANGE_NAME,CHANGE_price,CHANGE_theme,CHANGE_time



@dp.callback_query_handler(text = "change_channel_settings")
async def change_chanel(call: CallbackQuery):
    await call.message.edit_text(text='🦋Ваши канали', reply_markup=my_channels(call.from_user.id))



@dp.callback_query_handler(my_channels_callback.filter(lvl='1'))
async def change_chanel(call: CallbackQuery, callback_data:dict):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    print(channel[1])
    await call.message.edit_text(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))


@dp.callback_query_handler(my_channels_callback.filter(row="channel_id"),state=None)
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Ваш айди: {channel[1]}\nВведите ниже новый айди:\n⚠️Если вы не хотите ничего менять пришлите "-"')
    await CHANGE_ID.id.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]


@dp.message_handler(state=CHANGE_ID.id)
async def change_id(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            channel_id_new = message.text
                # pgbotdb.change_channel_id(channel_id, channel_id_new)
            await message.answer(f'Айди будет изменено на {channel_id_new}', reply_markup=back_to_channel_rows(change["channel_id"]))
            await state.finish()



@dp.callback_query_handler(my_channels_callback.filter(row="name"),state=None)
async def change_name___1(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Имя вашего канала: {channel[3]}\nВведите ниже новое имя:\n⚠️Если вы не хотите ничего менять пришлите "-"')
    await CHANGE_NAME.name.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]

@dp.message_handler(state=CHANGE_NAME.name)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            new_name = message.text
                # pgbotdb.change_channel_id(channel_id, channel_id_new)
            pgbotdb.channel_change_name(change["channel_id"], new_name)
            await message.answer(f'Имя изменено на {new_name}', reply_markup=back_to_channel_rows(change["channel_id"]))
            await state.finish()


@dp.callback_query_handler(my_channels_callback.filter(row="link"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Ссылка вашего канала: {channel[4]}\nВведите ниже новую ссылку:\n⚠️Если вы не хотите ничего менять пришлите "-"', disable_web_page_preview=True)
    await CHANGE_LINK.link.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
@dp.message_handler(state=CHANGE_LINK.link)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            new_link = message.text
                # pgbotdb.change_channel_id(channel_id, channel_id_new)
            pgbotdb.channel_change_link(change["channel_id"], new_link)
            await message.answer(f'Ссылка изменена на {new_link}', reply_markup=back_to_channel_rows(change["channel_id"]))
            await state.finish()


@dp.callback_query_handler(my_channels_callback.filter(row="comment"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Старый комент: {channel[6]}\nВведите новый коментарый:\n⚠️Если вы не хотите ничего менять пришлите "-"')
    await CHANGE_comment.comment.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
@dp.message_handler(state=CHANGE_comment.comment)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            new_comment = message.text
                # pgbotdb.change_channel_id(channel_id, channel_id_new)
            pgbotdb.channel_change_comment(change["channel_id"], new_comment)
            await message.answer(f'Комментарый изменен на {new_comment}', reply_markup=back_to_channel_rows(change["channel_id"]))
            await state.finish()

    
@dp.callback_query_handler(my_channels_callback.filter(row="description"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Старое описанные: {channel[5]}\nВведите новое описанные:\n⚠️Если вы не хотите ничего менять пришлите "-"')
    await CHANGE_description.description.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
@dp.message_handler(state=CHANGE_description.description)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            new_description = message.text
                # pgbotdb.change_channel_id(channel_id, channel_id_new)
            pgbotdb.channel_change_description(change["channel_id"], new_description)
            await message.answer(f'Описанные изменено на {new_description}', reply_markup=back_to_channel_rows(change["channel_id"]))
            await state.finish()


from keyboards.inline import end_setup_time
@dp.callback_query_handler(my_channels_callback.filter(row="times_for_posts"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(text= f'Ваше время постов {channel[9]}\nТеперь введите НОВОЕ время постов для своего канала через ",":\nПример:\n11:30, 14:00...')
    await CHANGE_time.time.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
@dp.message_handler(state=CHANGE_time.time)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            times = message.text.split(',')
            for time in times:
                time.strip('\n').strip(' ')
                await message.answer(text=time)
                print(times)
            async with state.proxy() as cond:
                cond["times"] = times
                await message.answer(f'Вы можете переотправить если допустили ошибку, или двигаться дальше по кнопке', reply_markup=end_setup_time)

@dp.callback_query_handler(text='end_setup_time', state=CHANGE_time.time)
async def end_time_for_posts(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as chan:
        pgbotdb.channel_change_times_for_posts(chan['channel_id'], json.dumps(chan['times']))
        channel = pgbotdb.select_channel(chan["channel_id"])
        await call.message.answer(text='🦋')
        await call.message.answer(text='Данные были изменени')
        await call.message.answer(text='🦋')
        await call.message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        await state.finish()


@dp.callback_query_handler(my_channels_callback.filter(row="conditions"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    conditions = pgbotdb.get_conditions(channel_id=channel[1])
    await call.message.answer(text= f'Ваши условия: {conditions}\nТеперь введите НОВЫЕ условия размещения для своего канала')
    await call.message.answer(text= 'Вводите условия через разделитель ","\n формат как ниже\nв топе/период - цена (без руб)')
    await call.message.answer(text="""Также возможно задать без удаление:\nБессрочно - 999\n⚠️Например: """)
    await call.message.answer(text="""1/24 - 200, 3/48 - 800, Бессрочно - 999""")
    await CHANGE_price.price.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
@dp.message_handler(state=CHANGE_price.price)
async def change_name(message:Message, state: FSMContext):
    async with state.proxy() as change:
        if message.text=='-':
            channel = pgbotdb.select_channel(change["channel_id"])
            await message.answer('ОК')
            await state.finish()
            await message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        else:
            conditions = message.text.split(',')
            cond = []
            print(conditions)
            for condition in conditions:
                condition = condition.split('-')
                condition_time = condition[0].replace(" ", "")
                price = condition[1].replace(" ","")
                await message.answer(f'{condition_time} -  {price} руб')
                cond.append([condition_time, price])
                print(condition_time, price)
            change['conditions'] = json.dumps(cond)
            await message.answer(f'Вы можете переотправить если допустили ошибку, или завершить ^ ^', reply_markup=end_channel_setup)
   
@dp.callback_query_handler(text='end_channel_setup', state=CHANGE_price.price)
async def banned_themes_gotovo(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as chan:
        pgbotdb.conditions_change_condition(channel_id=chan['channel_id'],
        conditions=chan['conditions'])
        channel = pgbotdb.select_channel(chan["channel_id"])
        await call.message.answer(text='🦋')
        await call.message.answer(text='Ваши условия были успешно обновлени🦋')
        await call.message.answer(text='🦋')
        await call.message.answer(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
        await state.finish()


from keyboards.inline import change_channel_theme
from loader import themes
@dp.callback_query_handler(my_channels_callback.filter(row="channels_theme"))
async def change_chanel(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    await call.message.answer(f'Старая тематика: {channel[7]}\nВыберите новую тематику через 2 секунди')
    await asyncio.sleep(2)
    await CHANGE_theme.theme.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
        await call.message.answer('Выберите новую тематику', reply_markup=change_channel_theme(themes=themes))

@dp.callback_query_handler(text_contains=('change_th'),state=CHANGE_theme.theme)
async def change_theme(call:CallbackQuery, state: FSMContext):
    new_theme = call.data.split(':')[1]
    async with state.proxy() as change:
        pgbotdb.channel_change_channels_theme(change['channel_id'], new_theme)
        await call.message.answer(f'Тема была изменена успешно\nНовая тематика канала {new_theme}', reply_markup=back_to_channel_rows(change['channel_id']))
        print(new_theme)
        await state.finish()

from keyboards.inline import banned_theme_callback
@dp.callback_query_handler(my_channels_callback.filter(row="change-baned_theme"))
async def change_banned1(call: CallbackQuery, callback_data:dict,state: FSMContext):
    channel = pgbotdb.select_channel(callback_data['channel_id'])
    try: 
        json.loads(channel[8])
        b_chnls = json.loads(channel[8])
    except json.decoder.JSONDecodeError:
        b_chnls = None
    await call.message.answer(f'Запрещенные тематики: {b_chnls}\nВыбрать можна будет через 2 секунди')
    await asyncio.sleep(2)
    await CHANGE_banned.banned.set()
    async with state.proxy() as change:
        change["channel_id"] = channel[1]
        change["change_list"] = []
        await call.message.answer('Выберите тематики', reply_markup=banned_theme_callback(copy.deepcopy(themes)))
        await CHANGE_banned.next()


@dp.callback_query_handler(text_contains='banned', state=CHANGE_banned.list)
async def change_banned(call: CallbackQuery,state: FSMContext):
    async with state.proxy() as change: 
        print(call.data)
        theme_name = call.data.split(":")[1]
        if theme_name not in change["change_list"]:
            change["change_list"].append(theme_name)
        else: change["change_list"].remove(theme_name)
        print(change["change_list"])
        await call.message.edit_text('Выберете запрещенные тематики', reply_markup=banned_theme_callback(copy.deepcopy(themes),change["change_list"]))
        
@dp.callback_query_handler(text='baned_next', state=CHANGE_banned.list)
async def banned_themes(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as change: 
        pgbotdb.channel_change_banned_themes(change['channel_id'], json.dumps(change["change_list"]))
        await call.message.answer(text= f'Запрещенные тематики изменени на:\n{change["change_list"]}',reply_markup=back_to_channel_rows(change['channel_id']))
        await state.finish()

from keyboards.inline import profile_kb_text
@dp.callback_query_handler(text='back_to_channels')
async def change_chanel(call: CallbackQuery):
    kb, text = profile_kb_text(call.from_user.id)
    await call.message.answer(text=text, reply_markup=kb)


@dp.callback_query_handler(text='back_to_my_channels')
async def change_chanel(call: CallbackQuery):
    await call.message.edit_text(text='🦋Ваши канали', reply_markup=my_channels(call.from_user.id))


@dp.callback_query_handler(text_contains='b_t_s_c')
async def back_to_sertain_channel(call:CallbackQuery):
    print(call.data)
    channel_id = call.data.split(':')[1]
    channel = pgbotdb.select_channel(channel_id)
    await call.message.edit_text(text=f"Канал: {channel[3]}", reply_markup=change_channel_parameters(channel[1]))
    