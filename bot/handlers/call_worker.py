from header import bot

from admin import *
from user import *


def call_work(call):
    bot.answer_callback_query(call.id)

    admin_menu(call)

    user_menu(call)
