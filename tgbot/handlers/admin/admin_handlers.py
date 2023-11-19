from tgbot.loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import types

from tgbot.data.bot_filter import IsAdmin

import os

from tgbot.database.db_logging import create_excel_file, get_reqx, update_reqx, get_userx, get_all_users_user_idx
from tgbot.buttons.admin.inline_admin import trans_edit_swipe_fp


@dp.message_handler(IsAdmin(), text='Вивантажити ДБ', state="*")
async def download_db(msg: Message, state: FSMContext):
    await state.finish()

    excel_file_path = create_excel_file()

    # Отправка файла пользователю
    with open(excel_file_path, 'rb') as excel_file:
        await msg.answer_document(excel_file)

    # Удаление временного Excel-файла
    os.remove(excel_file_path)


@dp.message_handler(IsAdmin(), text='Підтримка', state="*")
async def support_check(msg: Message, state: FSMContext):
    await state.finish()

    try:
        await msg.answer(
            "<b>Вибери клієнта</b>",
            reply_markup=trans_edit_swipe_fp(0),
        )
    except:
        await msg.answer('Запитань немає')


@dp.callback_query_handler(text_startswith="trans_edit_swipe", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    await state.finish()

    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>Вибери клієнта</b>",
        reply_markup=trans_edit_swipe_fp(remover),
    )


@dp.callback_query_handler(text_startswith="trans_edit_open", state="*")
async def user_purchase(call: CallbackQuery, state: FSMContext):
    await state.finish()

    id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    req = get_reqx(id=id)
    get_user = get_userx(user_id=req['user_id'])

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Закрити тікет', callback_data=f'close_question:{id}')
    ).add(
        types.InlineKeyboardButton('Назад', callback_data=f'trans_edit_swipe_fp:{remover}')
    )

    await call.message.edit_text(f"@{req['user_name']}\n"
                                 f"{get_user['contact_phone_number']}\n"
                                 f"{req['text']}", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='close_question', state="*")
async def close_question_call(call: CallbackQuery, state: FSMContext):
    await state.finish()

    try:
        id = call.data.split(":")[1]
        update_reqx(id, status='close')
        await call.message.edit_text('Тікет закритий')
    except:
        await call.message.answer('Помилка')


@dp.message_handler(IsAdmin(), text='Пост для всіх', state="*")
async def make_ad(message: Message, state: FSMContext):
    await state.finish()

    await message.answer('Write a post to promote it')

    await state.set_state('promotion')


@dp.message_handler(state='promotion')
async def if_need_photo(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Add photo')
    keyboard.row('Skip')
    keyboard.row('Cancel')


    await state.set_state('promotion_second')
    await state.update_data(text=message.text)
    await message.answer('Click the button below if you need to add a photo to your text', reply_markup=keyboard)


@dp.message_handler(text='Add photo', state='promotion_second')
async def get_photo(message: Message):
    keyboard = types.ReplyKeyboardRemove()

    await message.answer('Send the photo', reply_markup=keyboard)


@dp.message_handler(content_types=['photo'], state='promotion_second')
async def photo_processing(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Send')
    keyboard.row('Cancel')

    data = await state.get_data()
    text = data.get('text')
    file_id = message.photo[-1]
    photo = file_id.file_id

    await state.update_data(photo=photo)
    await message.answer('Your message, will look like?', reply_markup=keyboard)
    await message.answer_photo(photo, caption=text)


@dp.message_handler(text=['Skip', 'Send', 'Cancel'], state='promotion_second')
async def send_message_to_users(message: Message, state: FSMContext):
    user_ids = get_all_users_user_idx()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')


    if message.text == 'Cancel':
        await state.finish()
        await message.answer('/start')
    elif message.text == 'Send':
        try:
            for user_id, in user_ids:
                await bot.send_photo(user_id, photo, caption=text)
            await message.answer("Ads sent to users")
            await state.finish()
            await message.answer('/start')
        except Exception as e:
            print(e)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Send', 'Cancel')
        text = data.get('text')
        await state.set_state('check_if_good')
        await state.update_data(text=text)
        await message.answer('Your message, will look like?', reply_markup=keyboard)
        await message.answer(text)



@dp.message_handler(text=['Send', 'Cancel'], state='check_if_good')
async def check_if_good_text(message: Message, state: FSMContext):
    user_ids = get_all_users_user_idx()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    if message.text == 'Send':
        try:
            for user_id, in user_ids:
                await bot.send_message(user_id, text)
            await message.answer("Ads sent to users")
            await message.answer('/start')
        except Exception as e:
            print(e)
    else:
        await message.answer('/start')
