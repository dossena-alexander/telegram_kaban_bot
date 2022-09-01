import shutil, os
from header import adminMenu, userMenu
from header import userPicDB, adminPicDB, adminJokeDB, userJokeDB
from config import KEYS, PHOTO_CHANNEL, JOKE_CHANNEL

import server.admin.admin_utils as admin_utils
from server.admin.admin_utils.statistics import Statistics, Image_Statistic
from server.admin.admin_funcs import *


suggestions = admin_utils.Suggestions()


def admin_menu(call):
    if call.data == "STATISTICS":
        stats = Statistics()
        back = utils.InlineKeyboard()
        back.add_button(text="Количественная", call="IMG_STATISTICS")
        back.add_button(text="Назад", call="BACK_ADMIN")
        bot.edit_message_text(text=stats.get(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back.get(), parse_mode="html")
        del stats

    elif call.data == "IMG_STATISTICS":
        stats = Statistics()
        img_s = Image_Statistic()
        stats.get_img_stats(img_s)
        photo = img_s.path

        back = utils.InlineKeyboard()
        back.add_button(text="Назад", call="BACK_ADMIN")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_photo(call.message.chat.id, open(photo, 'rb'), caption='Количественная статистика', reply_markup=back)
        del stats
    
    elif call.data == "STOP_BOT":
        utils.log.info("ОСТАНОВКА БОТА")
        bot.stop_polling()

    elif call.data == "SUGGESTIONS":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.SUGGESTIONS)
        bot.edit_message_text(text="Предложения", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "UPLOAD_MENU_ADMIN":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.UPLOAD_MENU_ADMIN)
        keyboard.add_button(text="Назад", call="BACK_ADMIN")
        bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())

    elif call.data == "USER": 
        bot.edit_message_text(text=userMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.get_inline_keyboard())
    
    _admin_escape(call)

    _admin_notify_menu(call)

    _admin_upload_boars_menu(call)

    _admin_see_pictures_suggestions(call)

    _admin_see_jokes_suggestions(call)

    _admin_see_messages_from_users(call)


def _admin_escape(call):
    if call.data == "BACK_ADMIN":
        adminMenu.set_message("Админ меню")
        if suggestions.exist():
            adminMenu.set_message(suggestions.get_message())
        try:
            bot.edit_message_text(text=adminMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.get_inline_keyboard())
        except:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(text=adminMenu.message, chat_id=call.message.chat.id, reply_markup=adminMenu.get_inline_keyboard())
    

def _admin_notify_menu(call):
    if call.data == "NOTIFY_MENU": 
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.NOTIFY)
        keyboard.add_button("Назад", "BACK_ADMIN")
        bot.edit_message_text(text="Рассылка", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "NOTIFY":
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, admin_notify)

    elif call.data == "NOTIFY_BOT":
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, bot_notify)


def _admin_upload_boars_menu(call):
    if call.data == "UPLOAD_BOAR":
        keyboard = utils.ReplyKeyboard()
        keyboard.set(KEYS.CATEGORY)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(text="Выбери категорию кабана\nДля отмены нажми /brake", chat_id=call.message.chat.id, reply_markup=keyboard.get())
        bot.register_next_step_handler(call.message, choose_boar_category)

    elif call.data == "UPLOAD_PREM_BOAR":
        bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, upload_premium_wct)


def _admin_see_pictures_suggestions(call):
    if call.data == "SEE_PICTURES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_ACCEPT":
        photo_name = userPicDB.get_record(mesg.count)
        photo_id = userPicDB.get_record(mesg.count, col=1)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        adminPicDB.insert(photo_name, photo_id)
        bot.send_photo(PHOTO_CHANNEL, photo_id)
        userPicDB.delete_record(photo_name)
        shutil.move(PATH.RECIEVED_PHOTOS + photo_name, PATH.PHOTOS)
        
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_DELETE":    
        bot.delete_message(call.message.chat.id, call.message.message_id)
        os.remove(PATH.RECIEVED_PHOTOS + userPicDB.get_record(mesg.count))
        userPicDB.delete_record(userPicDB.get_record(mesg.count))
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)


def _admin_see_jokes_suggestions(call):
    if call.data == "SEE_JOKES": 
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_ACCEPT":
        joke = userJokeDB.get_record(mesg.count)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        adminJokeDB.new_record(joke)
        bot.send_message(JOKE_CHANNEL, joke)

        userJokeDB.delete_record(joke)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        userJokeDB.delete_record(userJokeDB.get_record(mesg.count))
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)


def _admin_see_messages_from_users(call):
    if call.data == "SEE_MESSAGES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if msgDB.msg_has_file_id(mesg.count):
            os.remove(PATH.RECIEVED_PHOTOS + msgDB.get_file_id(mesg.count))
        msgDB.delete_msg_and_file_id(mesg.count)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)
