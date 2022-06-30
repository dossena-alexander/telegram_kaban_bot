from header import bot, utils, config, msgDB, userDB, date, random, boarDB


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
            bot.send_message(message.chat.id, "Пришли еще картинку. Для отмены нажми /brake")
            del picDB
            bot.register_next_step_handler(message, uploadPicture)
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду картинку. Для отмены нажми /brake")
                bot.register_next_step_handler(message, uploadPicture)    
        else:      
            bot.send_message(message.chat.id, "Это не то, но я жду картинку. Для отмены нажми /brake")
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
                bot.send_message(message.chat.id, "Напиши анекдот. Для отмены нажми /brake")
                bot.register_next_step_handler(message, uploadJoke)
            else:
               bot.send_message(message.chat.id, "Это не то, но я жду твой анекдот. Для отмены нажми /brake") 
               bot.register_next_step_handler(message, uploadJoke)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Это не то, но я жду твой анекдот. Для отмены нажми /brake")
        bot.register_next_step_handler(message, uploadJoke)


def uploadMsg(message): 
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in config.word_filter:
                msgDB.newRecord(message.text)
                bot.send_message(message.chat.id, "Отправлено")
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду твое сообщение. Для отмены нажми /brake")
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
