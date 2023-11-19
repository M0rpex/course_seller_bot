from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def from_a_to_ya_ibtn():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton('Що я отримаю?', callback_data='help:what_get')
    ).add(
        InlineKeyboardButton('Придбати доступ', callback_data='help:buy_access')
    ).add(
        InlineKeyboardButton('Перейти на сайт', url='https://aprilparadise.com/')
    ).add(
        InlineKeyboardButton('Коли старт курсу?', callback_data='help:when_start')
    )

    return keyboard


def buy_access_ibtn():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton('Пакет самостійний', callback_data='buy_access:alone')
    ).add(
        InlineKeyboardButton('Робота з наставниками', callback_data='buy_access:trainer')
    ).add(
        InlineKeyboardButton('Персонально з Настею', callback_data='buy_access:individual')
    ).add(
        InlineKeyboardButton('Є питання?', callback_data='help:help')
    )

    return keyboard
