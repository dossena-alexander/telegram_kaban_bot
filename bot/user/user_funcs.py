from header import bot, utils, msgDB, userDB, date, random, boarDB, premiumBoarDB, suggestions
from config import PATH, ADMIN_ID, FILTER


def uploadPicture(message): 
    if message.content_type == 'photo':
        if message.media_group_id != None: # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadPicture)
        else:
            id = message.from_user.id
            picDB = utils.PicDB("accPics")
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            if id == ADMIN_ID: 
                upPic = utils.UploadPic(PATH.PHOTOS)
                txt = "Сохранил"
            else:
                upPic = utils.UploadPic(PATH.RECIEVED_PHOTOS)
                txt = "Добавлено на рассмотрение"
                picDB.setTableName("pics")
                suggestions.new_suggest()
            premiumProcess(message)
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            # saving photo id to DB of pics, either accepted pics table or pics table
            picDB.newRecord(file_info.file_path.replace('photos/', ''))
            upPic.upload(file, file_info)
            bot.send_message(message.chat.id, txt)
            bot.send_message(message.chat.id, "Пришли еще картинку.\nДля отмены нажми /brake")
            del picDB
            bot.register_next_step_handler(message, uploadPicture)
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду картинку.\nДля отмены нажми /brake")
                bot.register_next_step_handler(message, uploadPicture)    
        else:      
            bot.send_message(message.chat.id, "Это не то, но я жду картинку.\nДля отмены нажми /brake")
            bot.register_next_step_handler(message, uploadPicture)


def uploadJoke(message):
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in FILTER.COMMANDS:
                joke = message.text
                id = message.from_user.id 
                jokeDB = utils.JokeDB("adminJokes")
                if id == ADMIN_ID: 
                    txt = "Сохранил"
                else: 
                    jokeDB.setTableName('userJokes')
                    txt = "Добавлено на рассмотрение"
                    suggestions.new_suggest()
                premiumProcess(message)
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
            if message.text not in FILTER.COMMANDS:
                msgDB.newRecord(message.text)
                bot.send_message(message.chat.id, "Отправлено")
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду твое сообщение. Для отмены нажми /brake")
                bot.register_next_step_handler(message, uploadJoke)
        else:
            bot.send_message(message.chat.id, "Отменено")
    elif message.content_type == 'photo':
        upPic = utils.UploadPic(PATH.RECIEVED_PHOTOS)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file = bot.download_file(file_info.file_path)
        fileID = file_info.file_path.replace('photos/', '')
        upPic.upload(file, file_info)
        msgDB.newFileID(fileID)
        if message.caption != None:
            caption = message.caption
            msgDB.insertMsgForFileID(caption, fileID)
        bot.send_message(message.chat.id, "Отправил")
        del upPic
    else:
        bot.send_message(message.chat.id, "Это не то. Отправить можно только текст или картинку (необязательно с подписью). Напиши или отправь картинку. Для отмены нажми /brake")
        bot.register_next_step_handler(message, uploadMsg)

def getWct(message):
    """
    WCT is "Which Caban (boar) you Today is"
    every day user changes his "board id"
    if user in one day, when he used function in bot, will use wct again, wct give the same "boar id"
    """
    
    id = message.from_user.id 
    users = userDB.getUsersList()
    if id != ADMIN_ID and id not in users:
        bot.send_message(message.chat.id, "Ты не зарегистрировался. Нажми /auth, чтобы зарегистрироваться")
        return None
    else:
        now = date.today()
        now_day = now.day
        prev_day = userDB.getPrevDay(id)
        if userDB.checkPremium(id):
            db = premiumBoarDB
        else:
            db = boarDB
        if now_day == prev_day:
            boarID = userDB.getWctForUser(id)
            boar = db.getRecord(boarID)
            return open(PATH.WCT + boar, 'rb')
        else:
            userDB.setPrevDay(now_day, id)
            boarID = random.randint(0, db.getRecCount() - 1)
            userDB.setWctForUser(id, boarID)
            boar = db.getRecord(boarID)
            return open(PATH.WCT + boar, 'rb')


def premiumProcess(message):
    id = message.chat.id
    if userDB.checkPremium(id) == False:
        userDB.newUpload(id)
    if userDB.uploadsLimitReached(id):
        userDB.setPremium(id)
        boarID = random.randint(0, premiumBoarDB.getRecCount() - 1)
        userDB.setWctForUser(id, boarID)
        userDB.uploadsDel(id)
        bot.send_message(message.chat.id, "Поздравляю! Ты премиальный кабан!\nПроверь, нажми кнопку)")