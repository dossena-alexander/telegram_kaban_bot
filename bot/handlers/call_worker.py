from header import bot, utils, adminMenu, userMenu, userPicDB, shutil, os, adminPicDB, adminJokeDB, config, userJokeDB, msgDB, msgCounter, userSubMenu
from admin import *
from user import *


def callWorker(call):
    global msgCounter 

    bot.answer_callback_query(call.id)
#========================COMM====================================================    

    if call.data == 'Загрузить картинку': #+
        bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadPicture)

    elif call.data == 'Загрузить анекдот': #+
        bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadJoke)

#========================ADMIN_MENU====================================================

    elif call.data == "Статистика":
        stats = utils.Statistics()
        back = utils.InlineKeyboard()
        back.add(["Назад"])
        bot.edit_message_text(text=stats.get(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back.get(), parse_mode="html")
        del stats
    
    elif call.data == "Назад":
        bot.edit_message_text(text=adminMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.getInlineKeyboard())
    
    elif call.data == "Остановить бота": #+
        bot.answer_callback_query(call.id, 'Бот остановлен')
        utils.log.info("ОСТАНОВКА БОТА")
        bot.stop_polling()

    elif call.data == "Предложения":
        keyboard = utils.InlineKeyboard()
        keyboard.add(["Картинки", "Анекдоты"])
        keyboard.autoRow()
        keyboard.add(["Назад"])
        bot.edit_message_text(text="Предложения", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "Загрузка":
        keyboard = utils.InlineKeyboard()
        keyboard.add(["Загрузить картинку", "Загрузить анекдот", "Добавить кабана"])
        keyboard.autoRow()
        keyboard.add(["Назад"])
        bot.edit_message_text(text="Загрузка", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "Рассылка": #+
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, notify)
    
    elif call.data == "Пользователь": #+
        bot.edit_message_text(text=userMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.getInlineKeyboard())

    elif call.data == "Картинки":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, type="pic", db=userPicDB, keys=["выйти", "далее>", "Добавить", "Отменить"])

    elif call.data == "Добавить кабана":
        bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadWct)

#========================ADMIN_SEE_PICS===================================

    elif call.data == "далее>":
        msgCounter += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, type="pic", db=userPicDB, keys=["выйти", "далее>", "Добавить", "Отменить"])

    elif call.data == "Добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adminPicDB.newRecord(userPicDB.getRecord(msgCounter))
        shutil.move(config.recieved_photos_path + userPicDB.getPicID(msgCounter), config.photos_path)
        userPicDB.delRecord(userPicDB.getRecord(msgCounter))
        see(call.message, type="pic", db=userPicDB, keys=["выйти", "далее>", "Добавить", "Отменить"])

    elif call.data == "Отменить":    
        bot.delete_message(call.message.chat.id, call.message.message_id)
        os.remove(config.recieved_photos_path + userPicDB.getPicID(msgCounter))
        userPicDB.delRecord(userPicDB.getRecord(msgCounter))
        see(call.message, type="pic", db=userPicDB, keys=["выйти", "далее>", "Добавить", "Отменить"])

#========================ADMIN_SEE_JOKE===================================

    elif call.data == "Анекдоты": 
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", userJokeDB, ["Выйти", "Далее", "Принять","Удалить"])

    elif call.data == "Далее": #joke
        msgCounter += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", userJokeDB, ["Выйти", "Далее", "Принять","Удалить"])

    elif call.data == "Принять": #joke
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adminJokeDB.newRecord(userJokeDB.getRecord(msgCounter))
        userJokeDB.delRecord(userJokeDB.getRecord(msgCounter))
        see(call.message, "txt", userJokeDB, ["Выйти", "Далее", "Принять", "Удалить"])

    elif call.data == "Удалить": #joke
        bot.delete_message(call.message.chat.id, call.message.message_id)
        userJokeDB.delRecord(userJokeDB.getRecord(msgCounter))
        see(call.message, "txt", userJokeDB, ["Выйти", "Далее", "Принять", "Удалить"])

#========================ADMIN_SEE_MESSAGES===================================

    elif call.data == "Сообщения":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", msgDB, ["Выйти", "Далее>>", "Вычеркнуть"])

    elif call.data == "Далее>>": #msg
        msgCounter += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see(call.message, "txt", msgDB, ["Выйти", "Далее>>", "Вычеркнуть"])

    elif call.data == "Вычеркнуть": #msg
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msgDB.delRecord(msgDB.getRecord(msgCounter))
        see(call.message, "txt", msgDB, ["Выйти", "Далее>>", "Вычеркнуть"])

#========================USER_MENU====================================================
    elif call.data == "Загрузить":
        keyboard = utils.InlineKeyboard()
        keyboard.add(["Загрузить картинку", "Загрузить анекдот"])
        keyboard.autoRow()
        keyboard.add(["Вернуться"])
        bot.edit_message_text(text="Загрузка", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())

    elif call.data == "Сообщение админу":
        bot.edit_message_text(text="Напиши сообщение или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadMsg)

    elif call.data == "Кабаний перевод телеграмм":
        keyboard = utils.InlineKeyboard()
        keyboard.addUrlButton("Русский", "https://t.me/setlanguage/ru")
        keyboard.addUrlButton("Кабаний", "https://t.me/setlanguage/kabanchikoff")
        keyboard.add(["Вернуться"])
        bot.edit_message_text(text=userSubMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    elif call.data == "Вернуться":
        bot.edit_message_text(text=userMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.getInlineKeyboard())
