from aiogram.types import ReplyKeyboardMarkup

from datetime import datetime

from tgbot.data.config import get_admins


def user_main_btn(user_id):

    buy_access = '' if datetime.now().strftime('%d.%m') >= '26.11' else 'Придбати доступ'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Від А...Я', 'Є питання❔')
    keyboard.row(buy_access)
    keyboard.row('Написати Насті✉️', 'Instagram')

    if user_id in get_admins():
        keyboard.row('Вивантажити ДБ', 'Пост для всіх', 'Підтримка')

    return keyboard
