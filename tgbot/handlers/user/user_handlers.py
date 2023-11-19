from tgbot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import types

from datetime import datetime

from tgbot.database.db_logging import get_settings_allx, add_transx, add_questx
from tgbot.buttons.user.inline_user import from_a_to_ya_ibtn, buy_access_ibtn
from tgbot.buttons.reply_all import user_main_btn

#from tgbot.payment import Payment


@dp.message_handler(text='Від А...Я', state="*")
async def from_a_to_ya(msg: Message, state: FSMContext):
    await state.finish()

    await msg.answer('Що саме хотіла б?', reply_markup=from_a_to_ya_ibtn())


@dp.callback_query_handler(text_startswith='help', state="*")
async def help_call(call: CallbackQuery, state: FSMContext):
    await state.finish()

    action = call.data.split(':')[1]

    if action == 'what_get':
        await call.message.answer("Цей онлайн проект створений для дівчат, всіх і кожної.\n"
                                  "Аби кожна з нас мала змогу доторкнутись до себе справжньої, відчути свою силу, та почала #дихати_наповну!\n"
                                  "Ми з дівчатами-експертами  об'єднали наші знання, практику та досвід в одному місці, "
                                  "і запрошуємо тебе та кожну, хто бажає йти до себе справжньої та бажає змін як внутрішніх так і зовнішніх."
                                  "Тисни на 'Придбати доступ' та приєднуйся до дівчачого кола проекту 'Жінка від А..Я', ми чекаємо саме тебе!")
    elif action == 'buy_access':
        await call.message.edit_text('Обери свій пакет:', reply_markup=buy_access_ibtn())
    elif action == 'help':
        await call.message.delete()
        await call.message.answer("Напишіть та відправте запитання, яке бажаєте задати")
        await state.set_state('wait_question_state')
    elif action == 'when_start':
        if datetime.now().strftime('%d.%m.%y') >= '26.11.23':
            await call.message.answer('Чекай новини скоро❤️')
        else:
            await call.message.answer('27.11 зустрінемось з тобою')


@dp.message_handler(text='Придбати доступ', state="*")
async def buy_access_msg_handler(msg: Message, state: FSMContext):
    await state.finish()

    await msg.answer('Обери свій пакет:', reply_markup=buy_access_ibtn())


def check_non_cheap_day():
    if datetime.now().strftime('%d.%m') in get_settings_allx()[0]['cheap_day']:
        return True
    else:
        return False


@dp.callback_query_handler(text_startswith='buy_access', state='*')
async def but_access_call(call: CallbackQuery, state: FSMContext):
    await state.finish()

    action = call.data.split(":")[1]
    print(check_non_cheap_day())

    cost_dict = {'alone': 3712, 'trainer': 5588, 'individual': 9338}
    if check_non_cheap_day():
        cost_dict.update({'alone-non': 5625, 'trainer-non': 7500, 'individual-non': 11250})

    cost = cost_dict.get(action, 0)


    pack_dict = {
        'alone': "Самостійний\n"
                     "БЕЗ ЗВОРОТНЬОГО ЗВ'ЯЗКУ\n"
                     "<s>150$</s> 99$(3747 грн)\n\n"
                     "За 4 Тижні\n\n"
                     "- Доступ до всіх уроків та завдань\n"
                     "- Ефіри від головних експертів\n"
                     "- Бонуси та подарунки\n"
                     "- Доступ до курсу до кінця потоку - підтримка 24/7",
        'trainer': "Групові З Наставниками\n"
                   "ЗІ ЗВОРОТНІМ ЗВ'ЯЗКОМ ВІД НАСТАВНИКА\n"
                   "<s>200$</s> 149$(5640 грн)\n\n"
                   "За 4 Тижні\n\n"
                   "- Доступ до всіх уроків\n"
                   "- Перевірка домашнього завдання\n"
                   "- Участь в ефірах з експертами\n"
                   "- Окремі групи з наставниками\n"
                   "- Зворотній зв'язкок від експертів\n"
                   "- Бонуси та подарунки\n"
                   "- Доступ до уроків на 1 місяць після завершення потоку\n"
                   "- підтримка 24/7",
        'individual':   "Індивідуально З Анастасією\n"
                     "<s>300$</s> 249$(9425 грн)\n\n"
                     "За 4 Тижні\n\n"
                     "- Доступ до всіх уроків\n"
                     "- Перевірка домашнього завдання\n"
                     "- Участь в ефірах з експертами\n"
                     "- Зворотній зв'язкок від експертів\n"
                     "- Індивідуальна робота групи з Настею\n"
                     "- Бонуси та подарунки\n"
                     "- Доступ до уроків на 3 місяці після завершення потоку\n"
                     "- Бранч з @aprilparadise\n"
                     "- Індивідуальне меню від @aprilparadise\n"
                     "- підтримка 24/7",
    }

    pack = pack_dict.get(action)

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Придбати', callback_data=f'make_order:{action}')
    ).add(
        types.InlineKeyboardButton('Назад', callback_data='help:buy_access')
    )

    await call.message.edit_text(pack, reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='make_order', state="*")
async def make_order_call(call: CallbackQuery, state: FSMContext):
    await state.finish()

    action = call.data.split(':')[1]

    pack_dict = {
        'alone': "Самостійний\n"
                     "БЕЗ ЗВОРОТНЬОГО ЗВ'ЯЗКУ\n"
                     "<s>150$</s> 99$(3747 грн)\n\n"
                     "За 4 Тижні\n\n"
                     "- Доступ до всіх уроків та завдань\n"
                     "- Ефіри від головних експертів\n"
                     "- Бонуси та подарунки\n"
                     "- Доступ до курсу до кінця потоку - підтримка 24/7",
        'trainer': "Групові З Наставниками\n"
                   "ЗІ ЗВОРОТНІМ ЗВ'ЯЗКОМ ВІД НАСТАВНИКА\n"
                   "<s>200$</s> 149$(5640 грн)\n\n"
                   "За 4 Тижні\n\n"
                   "- Доступ до всіх уроків\n"
                   "- Перевірка домашнього завдання\n"
                   "- Участь в ефірах з експертами\n"
                   "- Окремі групи з наставниками\n"
                   "- Зворотній зв'язкок від експертів\n"
                   "- Бонуси та подарунки\n"
                   "- Доступ до уроків на 1 місяць після завершення потоку\n"
                   "- підтримка 24/7",
        'individual':   "Індивідуально З Анастасією\n"
                     "<s>300$</s> 249$(9425 грн)\n\n"
                     "За 4 Тижні\n\n"
                     "- Доступ до всіх уроків\n"
                     "- Перевірка домашнього завдання\n"
                     "- Участь в ефірах з експертами\n"
                     "- Зворотній зв'язкок від експертів\n"
                     "- Індивідуальна робота групи з Настею\n"
                     "- Бонуси та подарунки\n"
                     "- Доступ до уроків на 3 місяці після завершення потоку\n"
                     "- Бранч з @aprilparadise\n"
                     "- Індивідуальне меню від @aprilparadise\n"
                     "- підтримка 24/7",
    }

    pack = pack_dict.get(action)

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Оплачено', callback_data='make_payment')
    )

    await call.message.edit_text(pack)
    await call.message.answer("Реквізити для оплати:\n"
                              "Установа банку - ПриватБанк\n"
                              "МФО банку - <code>305299</code>\n"
                              "Отримувач платежу - РОМАНЕНКО АНАСТАСІЯ ВОЛОДИМИРІВНА\n"
                              "IBAN - <code>UA273354290000026002054018221</code>\n"
                              "Рахунок отримувача - <code>UA273354290000026002054018221</code>\n"
                              "Валюта рахунку - UAH\n"
                              "РНОКПП отримувача - <code>2858715080</code>", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='make_payment', state="*")
async def make_payment_call(call: CallbackQuery, state: FSMContext):

    print('1')
    await call.message.edit_text('Для завершення оплати, потрібно завантажити скріншот квитанції')
    await state.set_state('wait_photo_state')


@dp.message_handler(content_types=types.ContentType.PHOTO, state='wait_photo_state')
async def wait_photo(msg: Message, state: FSMContext):
    print('2')
    photo_id = msg.photo[-1].file_id


    # Отправляем фото
    await bot.send_photo(392401586, photo=photo_id, caption=f"TG: @{msg.from_user.username}\n")
    await msg.answer("Як тільки оплата буде перевірена з вами, зв'яжиться адміністратор")
    add_transx(msg.from_user.id, msg.from_user.username, datetime.now().strftime('%d.%m.%y'))
    await state.finish()



@dp.message_handler(text='Instagram', state="*")
async def give_instagram(msg: Message, state: FSMContext):
    await state.finish()

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Перейти', url='https://www.instagram.com/aprilparadise/')
    )

    await msg.answer('Інстаграм Насті', reply_markup=keyboard)


@dp.message_handler(text=['Написати Насті✉️', 'Є питання❔'], state="*")
async def give_instagram(msg: Message, state: FSMContext):
    await state.finish()

    await msg.answer("Напишіть та відправте запитання, яке бажаєте задати")
    await state.set_state('wait_question_state')


@dp.message_handler(state="wait_question_state")
async def wait_question(msg: Message, state: FSMContext):
    text = msg.text
    if msg.text == 'Назад':
        await state.finish()
        await msg.answer('Головне меню', reply_markup=user_main_btn(msg.from_user.id))
    else:
        try:
            add_questx(msg.from_user.id, msg.from_user.username, text, 'new', datetime.now().strftime("%d.%m"))
            await msg.answer('Ваше запитання було відправлено. Команда турботи, допоможе тобі, якнайшвидше')
            await state.finish()
        except:
            await msg.answer('Помилка')


@dp.message_handler(text="/info", state="*")
async def info_command(msg: Message, state: FSMContext):
    await state.finish()

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Договір оферти', url='https://aprilparadise.com/oferta/')
    )

    await msg.answer('<b>Aprilparadise</b>\n'
                     'ФОП Романенко А.В.\n\n'
                     'Контактні данні:\n'
                     'aprilparadise8@gmail.com\n\n', reply_markup=keyboard)


@dp.message_handler(text='/help', state="*")
async def help_command(msg: Message, state: FSMContext):
    await state.finish()

    await msg.answer('Бот створений для зручності в придбанні курсу.\n\n'
                     'Всі пакети курсу, можна побачити натиснувши кнопку на головному екрані "Придбати курс"\n\n'
                     'Щоб задати питання підтримці, потрібно натиснути кнопку на головному екрані "Є питання?"')

