from aiogram import Dispatcher

from tgbot.utils.functions import ExistsUserMiddleware
from tgbot.utils.throttling import ThrottlingMiddleware


# Подключение милдварей
def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(ExistsUserMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())