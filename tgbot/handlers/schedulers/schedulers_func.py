import asyncio
import random

from tgbot.loader import bot

from datetime import datetime, time

from tgbot.database.db_logging import get_all_users_user_idx, get_all_userx_where, get_advicexx


async def send_message_scheduler_evry():
    while True:
        current_time = datetime.now().time()
        scheduled_time = current_time.replace(second=0, microsecond=0)

        users = get_all_users_user_idx()

        # Проверяем, соответствует ли текущее время 7:00 или 15:00
        if scheduled_time == time(10, 0) or scheduled_time == time(13, 0):


            for user_id, in users:
                try:
                    await bot.send_message(user_id, f"<b>Повідомлення від Всесвіту</b>\n\n"
                                                    f"{get_advicexx(id=random.randint(1, 181))['advice']}")
                except:
                    print('error')

        # Ожидаем 1 минуту перед проверкой следующего времени
        await asyncio.sleep(60)


async def week_to_start_scheduler():
    while True:
        current_date = datetime.now().strftime('%d.%m')

        if current_date == '20.11':
            
            users = get_all_users_user_idx()

            for user_id, in users:
                try:
                    await bot.send_message(user_id, 'Рівно за тиждень ми з дівчатами починаємо! Ти з нами?')
                except:
                    print('error')
        await asyncio.sleep(43200)


async def msg_for_afk_user_scheduler():
    while True:
        users = get_all_userx_where(alarm_time=datetime.now().strftime('%d.%m'))

        if datetime.now().strftime('%d.%m') >= '26.11':

            for user_id in users:
                try:
                    await bot.send_message(user_id['user_id'], 'Ти ще не з нами? Можливо в тебе є запитання, то пиши їх в чат турботи і ми допоможемо!')
                except:
                    print('error')
        else:

            for user_id in users:
                try:
                    await bot.send_message(user_id['user_id'], 'Ти ще не з нами? Можливо в тебе є запитання, то пиши їх в чат турботи і ми допоможемо!❤️\n\nhttps://t.me/aprilparadise_supportteam')
                except:
                    print('error')
        await asyncio.sleep(43200)
