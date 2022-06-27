# v1.7.5.2
from header import *


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = utils.ReplyKeyboard()
    keyboard.add(config.startKeys)
    keyboard.autoRow()
    bot.send_message(message.chat.id, "Вечер в хату, кабан {0.first_name}!"
        .format(message.from_user, bot.get_me()), reply_markup=keyboard.get())


@bot.message_handler(commands=["auth"])
def auth(message):
    userID = message.from_user.id
    if userID == config.adminID:
        admin(message)
    else:
        usersList = userDB.getUsersList()
        if userID not in usersList:
            userDB.addUser(userID)
        user(message)


def admin(message):
    if new_suggestions.exist():
        adminMenu.setMsg(new_suggestions.getMsg())
    else:
        adminMenu.setMsg("Админ меню")
    bot.send_message(message.chat.id, adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard(), parse_mode="html")


def user(message):
    bot.send_message(message.chat.id, userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard()) 


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, helpMenu.getMsg(), parse_mode="html")


@bot.callback_query_handler(func=lambda call: True)
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


def uploadPicture(message): 
    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadPicture)
        else:
            id = message.from_user.id
            picDB = utils.PicDB("accPics")
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            if id == config.adminID: upPic = utils.UploadPic('admin'); txt = "Сохранил"
            else: upPic = utils.UploadPic('user'); txt = "Добавлено на рассмотрение"; picDB.setTableName("pics")
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            # saving photo id to DB of pics, either accepted pics table or pics table
            picDB.newRecord(file_info.file_path.replace('photos/', ''))
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, txt)
            bot.send_message(message.chat.id, "Пришли еще картинку или нажми /brake")
            del picDB
            bot.register_next_step_handler(message, uploadPicture)
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка!")
                bot.register_next_step_handler(message, uploadPicture)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка!")
            bot.register_next_step_handler(message, uploadPicture)


def uploadJoke(message):
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in config.word_filter:
                joke = message.text
                id = message.from_user.id 
                jokeDB = utils.JokeDB("adminJokes")
                if id == config.adminID: 
                    txt = "Сохранил"
                else: 
                    jokeDB.setTableName('userJokes')
                    txt = "Добавлено на рассмотрение"
                jokeDB.newRecord(joke)
                bot.send_message(message.chat.id, txt)
                bot.send_message(message.chat.id, "Напиши анекдот, или нажми /brake")
                bot.register_next_step_handler(message, uploadJoke)
            else:
               bot.send_message(message.chat.id, "Это не то, но я жду твой анекдот") 
               bot.register_next_step_handler(message, uploadJoke)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Только текст, пиши или нажми /brake")
        bot.register_next_step_handler(message, uploadJoke)


def uploadMsg(message): 
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in config.word_filter:
                msgDB.newRecord(message.text)
                bot.send_message(message.chat.id, "Отправлено")
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду твое сообщение")
                bot.register_next_step_handler(message, uploadJoke)
        else:
            bot.send_message(message.chat.id, "Отменено")
    elif message.content_type == 'photo':
        if message.photo.caption == '':
            caption = message.caption
            upPic = utils.UploadPic('')
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            fileID = file_info.file_path.replace('photos/', '')
            msgDB.newFileID(fileID)
            msgDB.insertMsgForFileID(caption, fileID)
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, "Отправил")
            del upPic
        else:
            upPic = utils.UploadPic('')
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            msgDB.newFileID(file_info.file_path.replace('photos/', ''))
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, "Отправил")
            del upPic


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


def getWct(message):
    """
    WCT is "Which Caban (boar) you Today is"
    every day user changes his "board id"
    if user in one day, when he used function in bot, will use wct again, wct give the same "boar id"
    """
    
    id = message.from_user.id 
    users = userDB.getUsersList()
    if id != config.adminID and id not in users:
        bot.send_message(message.chat.id, "Ты не зарегистрировался. Нажми /auth, чтобы зарегистрироваться")
        return None
    else:
        now = date.today()
        now_day = now.day
        prev_day = userDB.getPrevDay(id)
        if now_day == prev_day:
            boarID = userDB.getWctForUser(id)
            boar = boarDB.getID(boarID)
            return open(config.wct_path + boar, 'rb')
        else:
            userDB.setPrevDay(now_day, id)
            boarID = random.randint(0, boarDB.getRecCount() - 1)
            userDB.setWctForUser(id, boarID)
            boar = boarDB.getID(boarID)
            return open(config.wct_path + boar, 'rb')


@bot.message_handler(content_types="text") #+
def textWorker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        bot.send_photo(message.chat.id, 
        open(config.photos_path + adminPicDB.getPicID(recNum=random.randint(0, adminPicDB.getRecCount() - 1)), "rb"))
    elif msg == "анекдот":
        bot.send_message(message.chat.id, 
        adminJokeDB.getRecord(recNum=random.randint(0, adminJokeDB.getRecCount() - 1)))
    elif msg == "какой я кабан сегодня":
        if getWct(message) != None:
            bot.send_photo(message.chat.id, getWct(message))



if __name__ == "__main__":
    try:
        print("BOT STARTED")
        utils.log.info("BOT STARTED")
        bot.polling()
    except:
        print("BOT reSTARTED")
        utils.log.info("BOT reSTARTED")
        bot.polling()