from header import adminMenu, userMenu
from header import suggestions
from header import userPicDB, adminPicDB, adminJokeDB, userJokeDB
from header import shutil, os, mesg
from config import KEYS

from admin.admin_funcs import *


class Admin():
    @staticmethod
    def admin_menu(call):
        if call.data == "STATISTICS":
            stats = utils.Statistics()
            back = utils.InlineKeyboard()
            back.add_button(text="Назад", call="BACK_ADMIN")
            bot.edit_message_text(text=stats.get(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back.get(), parse_mode="html")
            del stats
        
        elif call.data == "STOP_BOT":
            utils.log.info("ОСТАНОВКА БОТА")
            bot.stop_polling()

        elif call.data == "SUGGESTIONS":
            keyboard = utils.InlineKeyboard()
            keyboard.set_keyboard(KEYS.SUGGESTIONS)
            bot.edit_message_text(text="Предложения", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
        
        elif call.data == "UPLOAD_MENU_ADMIN":
            keyboard = utils.InlineKeyboard()
            keyboard.set_keyboard(KEYS.UPLOAD_MENU_ADMIN)
            keyboard.add_button(text="Назад", call="BACK_ADMIN")
            bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())

        elif call.data == "USER": 
            bot.edit_message_text(text=userMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.get_inline_keyboard())
        
        Admin._admin_escape(call)

        Admin._admin_notify_menu(call)

        Admin._admin_upload_boars_menu(call)

        Admin._admin_see_pictures_suggestions(call)

        Admin._admin_see_jokes_suggestions(call)

        Admin._admin_see_messages_from_users(call)


    @staticmethod
    def _admin_escape(call):
        if call.data == "BACK_ADMIN":
            adminMenu.set_message("Админ меню")
            if suggestions.exist():
                adminMenu.set_message(suggestions.get_message())
            bot.edit_message_text(text=adminMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.get_inline_keyboard())
        

    @staticmethod
    def _admin_notify_menu(call):
        if call.data == "NOTIFY_MENU": 
            keyboard = utils.InlineKeyboard()
            keyboard.set_keyboard(KEYS.NOTIFY)
            keyboard.add_button("Назад", "BACK_ADMIN")
            bot.edit_message_text(text="Рассылка", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
        
        elif call.data == "NOTIFY":
            bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, admin_notify)

        elif call.data == "NOTIFY_BOT":
            bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, bot_notify)


    @staticmethod
    def _admin_upload_boars_menu(call):
        if call.data == "UPLOAD_BOAR":
            keyboard = utils.ReplyKeyboard()
            keyboard.set_keyboard(KEYS.CATEGORY)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(text="Выбери категорию кабана\nДля отмены нажми /brake", chat_id=call.message.chat.id, reply_markup=keyboard.get())
            bot.register_next_step_handler(call.message, choose_boar_category)

        elif call.data == "UPLOAD_PREM_BOAR":
            bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, upload_premium_wct)


    @staticmethod
    def _admin_see_pictures_suggestions(call):
        if call.data == "SEE_PICTURES":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

        elif call.data == "PIC_FURTHER":
            mesg.count += 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

        elif call.data == "PIC_ACCEPT":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            adminPicDB.new_record(userPicDB.get_record(mesg.count))
            shutil.move(PATH.RECIEVED_PHOTOS + userPicDB.get_record(mesg.count), PATH.PHOTOS)
            userPicDB.delete_record(userPicDB.get_record(mesg.count))
            see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

        elif call.data == "PIC_DELETE":    
            bot.delete_message(call.message.chat.id, call.message.message_id)
            os.remove(PATH.RECIEVED_PHOTOS + userPicDB.get_record(mesg.count))
            userPicDB.delete_record(userPicDB.get_record(mesg.count))
            see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)


    @staticmethod
    def _admin_see_jokes_suggestions(call):
        if call.data == "SEE_JOKES": 
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

        elif call.data == "JOKE_FURTHER":
            mesg.count += 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

        elif call.data == "JOKE_ACCEPT":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            adminJokeDB.new_record(userJokeDB.get_record(mesg.count))
            userJokeDB.delete_record(userJokeDB.get_record(mesg.count))
            see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

        elif call.data == "JOKE_DELETE":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            userJokeDB.delete_record(userJokeDB.get_record(mesg.count))
            see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)


    @staticmethod
    def _admin_see_messages_from_users(call):
        if call.data == "SEE_MESSAGES":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_messages_to_admin(call.message, KEYS.MSG_SEE)

        elif call.data == "MSG_FURTHER":
            mesg.count += 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
            see_messages_to_admin(call.message, KEYS.MSG_SEE)

        elif call.data == "MSG_DELETE":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if msgDB.msg_has_file_id(mesg.count):
                os.remove(PATH.RECIEVED_PHOTOS + msgDB.get_file_id(mesg.count))
            msgDB.delete_msg_and_file_id(mesg.count)
            see_messages_to_admin(call.message, KEYS.MSG_SEE)
