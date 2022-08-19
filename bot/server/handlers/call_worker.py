from header import bot

from client.admin_menu import admin_menu
from client.user_menu import user_menu


def call_work(call):
    bot.answer_callback_query(call.id)

    admin_menu(call)

    user_menu(call)
