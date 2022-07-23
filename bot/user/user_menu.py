from header import userMenu, userSubMenu
from config import KEYS

from user.user_funcs import *

class User():
    def user_menu(call):
        if call.data == "UPLOAD_MENU_USER":
            keyboard = utils.InlineKeyboard()
            keyboard.set_keyboard(KEYS.UPLOAD_MENU_USER)
            bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())

        elif call.data == "MESSAGE_TO_ADMIN":
            bot.edit_message_text(text="Напиши сообщение или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, "Отправить можно только текст или картинку (необязательно с подписью)")
            bot.register_next_step_handler(call.message, upload_message_to_admin)

        elif call.data == "TRANSLATE":
            keyboard = utils.InlineKeyboard()
            keyboard.add_url_button("Русский", "https://t.me/setlanguage/ru")
            keyboard.add_url_button("Кабаний", "https://t.me/setlanguage/kabanchikoff")
            keyboard.add_button(text="Назад", call="BACK_USER")
            bot.edit_message_text(text=userSubMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
        
        elif call.data == "ACHIEVEMENTS":
            achievements = utils.Achievements(call.message.chat.id)
            keyboard = utils.InlineKeyboard()
            keyboard.add_button(text="Назад", call="BACK_USER")
            bot.edit_message_text(text=achievements.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")

        elif call.data == "PREMIUM":
            premiumMenu = utils.PremiumMenu(call.message.chat.id)
            keyboard = utils.InlineKeyboard()
            keyboard.add_button(text="О премиум", call="ABOUT_PREMIUM")
            keyboard.add_button(text="Назад", call="BACK_USER")
            bot.edit_message_text(text=premiumMenu.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")
        
        User._user_escape(call)

        User._user_premium_menu(call)

        User._user_upload_menu(call)


    @staticmethod
    def _user_escape(call):
        if call.data == "BACK_USER":
            bot.edit_message_text(text=userMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.get_inline_keyboard())


    @staticmethod
    def _user_premium_menu(call):
        if call.data == "ABOUT_PREMIUM":
            text = utils.PremiumMenu.get_text_about()
            keyboard = utils.InlineKeyboard()
            keyboard.add_button(text="Назад", call="BACK_USER")
            bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")


    @staticmethod
    def _user_upload_menu(call):
        if call.data == 'UPLOAD_PICTURE':
            bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, upload_photo)

        elif call.data == 'UPLOAD_JOKE':
            bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, upload_joke)
