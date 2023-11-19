from tgbot.loader import dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import types

from tgbot.database.db_logging import get_userx, update_userx
from tgbot.buttons.reply_all import user_main_btn


@dp.message_handler(commands=['start'], state="*")
async def user_start(msg: Message, state: FSMContext):
    await state.finish()

    start_param = msg.get_args()

    if get_userx(user_id=msg.from_user.id)['contact_name'] is None or get_userx(user_id=msg.from_user.id)[
        'contact_phone_number'] is None:
        await msg.answer('Привіт люба 🌹\n'
                         'Дякую за довіру та вітаю тебе в своєму просторі 🫶\n'
                         'Цей проект, який стане твоєю підтримкою, опорою і шляхом до справжньої себе 🤗')
        await msg.answer('Як тебе звуть?', reply_markup=user_main_btn(msg.from_user.id))
        await state.set_state('get_name_state')

    elif start_param:
        await msg.answer('1')
    else:
        name = 'красуня' if get_userx(user_id=msg.from_user.id)['contact_name'] is None else \
            get_userx(user_id=msg.from_user.id)['contact_name']
        await msg.answer(
            f'Привіт {name}! Це @aprilparadise Ми вже познайомились, а отже можемо йти далі, якщо потрібна буде допомога - натискай "Є питання?" та мої феї попіклуються про тебе',
            reply_markup=user_main_btn(msg.from_user.id))


@dp.message_handler(state="get_name_state")
async def get_name(msg: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Поділитись номером телефону', request_contact=True)
    keyboard.add(btn)

    name = msg.text

    try:
        update_userx(msg.from_user.id, contact_name=name)
        await msg.answer('Тепер залиш свій номер телефону(Починаючи з 0, або натисни кнопку під полем вводу)',
                         reply_markup=keyboard)
        await state.set_state('wait_number_state')
    except Exception as e:
        await msg.answer('Сталася помилка')


@dp.message_handler(state="wait_number_state")
@dp.message_handler(content_types=types.ContentType.CONTACT, state="wait_number_state")
async def handle_contact(msg: Message, state: FSMContext):
    contact = msg.contact

    if contact is None:
        if len(msg.text) == 10:
            try:
                update_userx(msg.from_user.id, contact_phone_number=msg.text)
                update_userx(msg.from_user.id, alarm_time=None)
                name = 'красуня' if get_userx(user_id=msg.from_user.id)['contact_name'] is None else \
                    get_userx(user_id=msg.from_user.id)['contact_name']

                await msg.answer(
                    f'Привіт {name}! Це @aprilparadise Ми вже познайомились, а отже можемо йти далі, якщо потрібна буде допомога - натискай "Є питання?" та мої феї попіклуються про тебе',
                    reply_markup=user_main_btn(msg.from_user.id))
                await state.finish()
            except Exception:
                await msg.answer('Сталася помилка')
        else:
            await msg.answer('Номер телефону має містити 10 цифр.(Формат: 0XXXXXXXXX)')
    else:
        try:
            update_userx(msg.from_user.id, contact_phone_number=contact.phone_number)
            update_userx(msg.from_user.id, alarm_time=None)
            name = 'красуня' if get_userx(user_id=msg.from_user.id)['contact_name'] is None else \
                get_userx(user_id=msg.from_user.id)['contact_name']

            await msg.answer(
                f'Привіт {name}! Це @aprilparadise Ми вже познайомились, а отже можемо йти далі, якщо потрібна буде допомога - натискай "Є питання?" та мої феї попіклуються про тебе',
                reply_markup=user_main_btn(msg.from_user.id))
            await state.finish()
        except Exception:
            await msg.answer('Сталася помилка')
