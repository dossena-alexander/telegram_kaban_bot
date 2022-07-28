from header import bot

from admin import *
from user import *


def call_work(call):
    bot.answer_callback_query(call.id)

    Admin.admin_menu(call)

    User.user_menu(call)
