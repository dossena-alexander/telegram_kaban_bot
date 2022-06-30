from header import bot, utils, boarDB, userDB, config, userPicDB, msgCounter


def uploadWct(message):
    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic (in future)
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadWct)
        else:
            upPic = utils.UploadPic('wct')
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            boarDB.newRecord(file_info.file_path.replace('photos/', ''))
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, "Сохранил")
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
                bot.register_next_step_handler(message, uploadWct)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
            bot.register_next_step_handler(message, uploadWct)


def notify(message):
    if message.content_type == 'text':
        msg = message.text
        if msg != '/brake':
            if msg not in config.word_filter:
                users = userDB.getUsersList()
                if len(users) != 0:
                    for id in users:
                        bot.send_message(id, 
                        "<b>Сообщение от админа:</b>\n" + msg, parse_mode="html")
                else:
                    bot.send_message(config.adminID, "Пользователей для рассылки нет")
            else:
                bot.send_message(config.adminID, "Это не то, но я жду твое сообщение")
                bot.register_next_step_handler(message, notify)
        else:
            bot.send_message(config.adminID, "Отменено")


def see(message, type: str, db: utils.DB, keys: list):
    global msgCounter

    stand_keyboard = utils.InlineKeyboard()
    stand_keyboard.add(keys)
    stand_keyboard.autoRow()
    back_keyboard = utils.InlineKeyboard()
    back_keyboard.add(["Назад"])

    # get records len with DB method
    record_len = db.getRecCount()
    if record_len != 0:
        if msgCounter < record_len: # msgCounter is counter which increase and count every each record 
            if type == "txt":
                bot.send_message(message.chat.id,
                    f"{record_len} записей\n" +
                    f"{db.getRecord(recNum=msgCounter)}",
                    reply_markup=stand_keyboard.get())
            else:
                bot.send_photo(message.chat.id, 
                    open(config.recieved_photos_path + userPicDB.getPicID(msgCounter), "rb"),
                    reply_markup=stand_keyboard.get(),
                    caption=f"{record_len} записей")
        else:
            msgCounter = 0
            bot.send_message(
                message.chat.id,
                "Сообщения кончились",
                reply_markup=back_keyboard.get())
    else:
        bot.send_message(message.chat.id, "Сообщений нет", reply_markup=back_keyboard.get())
