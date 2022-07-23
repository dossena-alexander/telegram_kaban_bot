from header import boarDB, premiumBoarDB, userDB, msgDB, boarsCategories
from header import bot, utils, mesg
from config import PATH, ADMIN_ID, FILTER

def choose_boar_category(message):
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in FILTER.COMMANDS:
                boar_category = message.text.lower()
                bot.send_message(message.chat.id, "Теперь загрузи кабана.\nДля отмены нажми /brake")
                bot.register_next_step_handler(message, _upload_wct, boar_category)
            else:
               bot.send_message(message.chat.id, "Это не то, но я жду ответ.\nДля отмены нажми /brake") 
               bot.register_next_step_handler(message, choose_boar_category)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Это не то, но я жду ответ.\nДля отмены нажми /brake")
        bot.register_next_step_handler(message, choose_boar_category)


def _upload_wct(message, boar_category) -> None:
    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic (in future)
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, _upload_wct, boar_category)
        else:
            upPic = utils.UploadPic(PATH.WCT)
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            boar = file_info.file_path.replace('photos/', '')
            boarDB.new_record(boar)
            boarsCategories.new_boar(boar_category, boar)
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, "Сохранил")
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
                bot.register_next_step_handler(message, _upload_wct, boar_category)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
            bot.register_next_step_handler(message, _upload_wct, boar_category)


def upload_premium_wct(message) -> None:
    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic (in future)
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, upload_premium_wct)
        else:
            upPic = utils.UploadPic(PATH.WCT)
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            boar = file_info.file_path.replace('photos/', '')
            premiumBoarDB.new_record(boar)
            boarsCategories.new_boar("premium", boar)
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, "Сохранил")
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
                bot.register_next_step_handler(message, upload_premium_wct)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
            bot.register_next_step_handler(message, upload_premium_wct)


def admin_notify(message) -> None:
    if message.content_type == 'text':
        msg = message.text
        if msg != '/brake':
            if msg not in FILTER.COMMANDS:
                users = userDB.get_users_list()
                if len(users) != 0:
                    for id in users:
                        bot.send_message(id, 
                        "<b>Сообщение от админа:</b>\n" + msg, parse_mode="html")
                else:
                    bot.send_message(ADMIN_ID, "Пользователей для рассылки нет")
            else:
                bot.send_message(ADMIN_ID, "Это не то, но я жду твое сообщение")
                bot.register_next_step_handler(message, admin_notify)
        else:
            bot.send_message(ADMIN_ID, "Отменено")


def bot_notify(message) -> None:
    if message.content_type == 'text':
        msg = message.text
        if msg != '/brake':
            if msg not in FILTER.COMMANDS:
                users = userDB.get_users_list()
                if len(users) != 0:
                    for id in users:
                        bot.send_message(id, msg, parse_mode="html")
                else:
                    bot.send_message(ADMIN_ID, "Пользователей для рассылки нет")
            else:
                bot.send_message(ADMIN_ID, "Это не то, но я жду твое сообщение")
                bot.register_next_step_handler(message, bot_notify)
        else:
            bot.send_message(ADMIN_ID, "Отменено")


def see_suggestions(message, type: str, db: utils.DB, keys: dict) -> None:
    stand_keyboard = utils.InlineKeyboard()
    stand_keyboard.set_keyboard(keys)

    back_keyboard = utils.InlineKeyboard()
    back_keyboard.add_button(text="Назад", call="BACK_ADMIN")

    # get records len with DB method
    record_len = db.get_records_count()
    if record_len != 0:
        if mesg.count < record_len: # msgCounter is counter which increase and count every each record 
            if type == "txt":
                bot.send_message(message.chat.id,
                    f"{record_len} записей\n" +
                    f"{db.get_record(row=mesg.count)}",
                    reply_markup=stand_keyboard.get())
            else:
                bot.send_photo(message.chat.id, 
                    open(PATH.RECIEVED_PHOTOS + db.get_record(mesg.count), "rb"),
                    reply_markup=stand_keyboard.get(),
                    caption=f"{record_len} записей")
        else:
            mesg.count = 0
            bot.send_message(
                message.chat.id,
                "Сообщения кончились",
                reply_markup=back_keyboard.get())
    else:
        bot.send_message(message.chat.id, "Сообщений нет", reply_markup=back_keyboard.get())


def see_messages_to_admin(message, keys: dict) -> None:
    stand_keyboard = utils.InlineKeyboard()
    stand_keyboard.set_keyboard(keys)

    back_keyboard = utils.InlineKeyboard()
    back_keyboard.add_button(text="Назад", call="BACK_ADMIN")

    # get records len with DB method
    record_len = msgDB.get_records_count()
    if record_len != 0:
        if mesg.count < record_len: # msgCounter is counter which increase and count every each record 
            if msgDB.msg_has_file_id(mesg.count):
                bot.send_photo(message.chat.id, 
                    open(PATH.RECIEVED_PHOTOS + msgDB.get_file_id(mesg.count), "rb"),
                    reply_markup=stand_keyboard.get(),
                    caption=f"{record_len} записей\n{msgDB.get_record(mesg.count)}")
            else:
                bot.send_message(message.chat.id,
                    f"{record_len} записей\n" +
                    f"{msgDB.get_record(row=mesg.count)}",
                    reply_markup=stand_keyboard.get())
        else:
            mesg.count = 0
            bot.send_message(
                message.chat.id,
                "Сообщения кончились",
                reply_markup=back_keyboard.get())
    else:
        bot.send_message(message.chat.id, "Сообщений нет", reply_markup=back_keyboard.get())