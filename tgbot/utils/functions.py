from tgbot.database.db_logging import get_userx, add_userx
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from datetime import datetime, timedelta


class ExistsUserMiddleware(BaseMiddleware):
    def __init__(self):
        self.prefix = "key_prefix"
        super(ExistsUserMiddleware, self).__init__()


    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = message.from_user

        await self.add_log_user(user)


    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        user = query.from_user

        await self.add_log_user(user)


    async def add_log_user(self, user):
        user_login = user.username
        user_name = user.full_name
        get_user = get_userx(user_id=user.id)
        date_now = datetime.now()
        date_tomorrow = date_now + timedelta(days=1)
        date = date_tomorrow.strftime('%d.%m')
        reg_date = datetime.now().strftime('%d.%m.%y')

        if get_user is None:
            add_userx(reg_date, user.id, user_login, user_name, date)

