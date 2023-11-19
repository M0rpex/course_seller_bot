import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.database.db_logging import *


def trans_edit_swipe_fp(remover):
    keyboard = InlineKeyboardMarkup()

    get_trans = get_req_allx(status='new')

    remover_page = len(get_trans) + (10 - (len(get_trans) % 10))

    if remover >= len(get_trans): remover -= 10

    for count, a in enumerate(range(remover, len(get_trans))):
        if count < 10:
            keyboard.add(ikb(
                f"{get_trans[a]['date']} | {get_trans[a]['user_name']}",
                callback_data=f"trans_edit_open:{get_trans[a]['id']}:{remover}",
            ))
    if len(get_trans) <= 10:
        pass
    elif len(get_trans) > 10 and remover < 10:
        if len(get_trans) > 20:
            keyboard.add(
                ikb(f"1/{math.ceil(len(get_trans) / 10)}", callback_data="..."),
                ikb("➡", callback_data=f"trans_edit_swipe:{remover + 10}"),
                ikb("⏩", callback_data=f"trans_edit_swipe:{remover_page}"),
            )
        else:
            keyboard.add(
                ikb(f"1/{math.ceil(len(get_trans) / 10)}", callback_data="..."),
                ikb("➡", callback_data=f"trans_edit_swipe:{remover + 10}")
            )
    elif remover + 10 >= len(get_trans):
        if len(get_trans) > 20:
            keyboard.add(
                ikb("⏪", callback_data=f"trans_edit_swipe:0"),
                ikb("⬅", callback_data=f"trans_edit_swipe:{remover - 10}"),
                ikb(f"{str(remover + 10)[:-1]}/{math.ceil(len(get_trans) / 10)}", callback_data="..."),
            )
        else:
            keyboard.add(
                ikb("⬅", callback_data=f"trans_edit_swipe:{remover - 10}"),
                ikb(f"{str(remover + 10)[:-1]}/{math.ceil(len(get_trans) / 10)}", callback_data="...")
            )
    else:
        if len(get_trans) > 20:
            keyboard.add(
                ikb("⏪", callback_data=f"trans_edit_swipe:0"),
                ikb("⬅", callback_data=f"trans_edit_swipe:{remover - 10}"),
                ikb(f"{str(remover + 10)[:-1]}/{math.ceil(len(get_trans) / 10)}", callback_data="..."),
                ikb("➡", callback_data=f"trans_edit_swipe:{remover + 10}"),
                ikb("⏩", callback_data=f"trans_edit_swipe:{remover_page}"),
            )
        else:
            keyboard.add(
                ikb("⬅", callback_data=f"trans_edit_swipe:{remover - 10}"),
                ikb(f"{str(remover + 10)[:-1]}/{math.ceil(len(get_trans) / 10)}", callback_data="..."),
                ikb("➡", callback_data=f"trans_edit_swipe:{remover + 10}"),
            )

    return keyboard

