from header import bot, utils 
from header import userSubMenu, new_suggestions, adminMenu, userMenu, userPicDB, adminPicDB, adminJokeDB, userJokeDB, msgDB
from header import mesg, shutil, os
from config import PATH, KEYS
from admin import *
from user import *


def callWorker(call):
    bot.answer_callback_query(call.id)
#========================COMM====================================================    

    if call.data == 'UPLOAD_PICTURE':
        bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadPicture)

    elif call.data == 'UPLOAD_JOKE':
        bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadJoke)

#========================ADMIN_MENU====================================================

    elif call.data == "STATISTICS":
        stats = utils.Statistics()
        back = utils.InlineKeyboard()
        back.add_button(text="Назад", call="BACK_ADMIN")
        bot.edit_message_text(text=stats.get(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back.get(), parse_mode="html")
        del stats
    
    elif call.data == "BACK_ADMIN":
        if new_suggestions.exist():
            adminMenu.setMsg(new_suggestions.getMsg())
        else:
            adminMenu.setMsg("Админ меню")
        bot.edit_message_text(text=adminMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.getInlineKeyboard())
    
    elif call.data == "STOP_BOT":
        bot.answer_callback_query(call.id, 'Бот остановлен')
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
    
    elif call.data == "NOTIFY": #+
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, notify)
    
    elif call.data == "USER": #+
        bot.edit_message_text(text=userMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.getInlineKeyboard())

    elif call.data == "UPLOAD_BOAR":
        bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadWct)

#========================ADMIN_SEE_PICS===================================

    elif call.data == "SEE_PICTURES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_ACCEPT":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adminPicDB.newRecord(userPicDB.getRecord(mesg.count))
        shutil.move(PATH.RECIEVED_PHOTOS + userPicDB.getPicID(mesg.count), PATH.PHOTOS)
        userPicDB.delRecord(userPicDB.getRecord(mesg.count))
        see(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_DELETE":    
        bot.delete_message(call.message.chat.id, call.message.message_id)
        os.remove(PATH.RECIEVED_PHOTOS + userPicDB.getPicID(mesg.count))
        userPicDB.delRecord(userPicDB.getRecord(mesg.count))
        see(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

#========================ADMIN_SEE_JOKE===================================

    elif call.data == "SEE_JOKES": 
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_ACCEPT":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adminJokeDB.newRecord(userJokeDB.getRecord(mesg.count))
        userJokeDB.delRecord(userJokeDB.getRecord(mesg.count))
        see(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        userJokeDB.delRecord(userJokeDB.getRecord(mesg.count))
        see(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

#========================ADMIN_SEE_MESSAGES===================================

    elif call.data == "SEE_MESSAGES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", msgDB, KEYS.MSG_SEE)

    elif call.data == "MSG_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", msgDB, KEYS.MSG_SEE)

    elif call.data == "MSG_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msgDB.delRecord(msgDB.getRecord(mesg.count))
        see(call.message, "txt", msgDB, KEYS.MSG_SEE)

#========================USER_MENU====================================================
    elif call.data == "UPLOAD_MENU_USER":
        keyboard = utils.InlineKeyboard()
        keyboard.set_keyboard(KEYS.UPLOAD_MENU_USER)
        bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())

    elif call.data == "MESSAGE_TO_ADMIN":
        bot.edit_message_text(text="Напиши сообщение или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadMsg)

    elif call.data == "TRANSLATE":
        keyboard = utils.InlineKeyboard()
        keyboard.add_url_button("Русский", "https://t.me/setlanguage/ru")
        keyboard.add_url_button("Кабаний", "https://t.me/setlanguage/kabanchikoff")
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=userSubMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "BACK_USER":
        bot.edit_message_text(text=userMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.getInlineKeyboard())
