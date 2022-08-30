from io import BufferedReader
from server import utils
from header import bot, msgDB, userDB
from config import PATH, ADMIN_ID, FILTER, PHOTO_CHANNEL, JOKE_CHANNEL
from server.utils.db import BoarsCategories
from server.admin.admin_utils.suggestions import Suggestions
from server.user.user_utils import funcs, premium, achievements
from server.user.user_utils.achievements import translate_category


suggestions = Suggestions()


def upload_photo(message) -> None: 
    if message.content_type == 'photo':
        if message.media_group_id != None: # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, upload_photo)
        else:
            user_id = message.from_user.id
            user_name = message.from_user.username
            picDB = utils.PicDB("accPics")
            upPic = utils.UploadPic(PATH.PHOTOS)
            txt = "Сохранил"
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            if user_id != ADMIN_ID:     
                upPic = utils.UploadPic(PATH.RECIEVED_PHOTOS)
                txt = "Добавлено на рассмотрение"
                picDB.set_table("pics")
                suggestions.new_suggest()
            premium.new_upload_for_user(message)
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.replace('photos/', '')
            # saving photo id to DB of pics, either accepted pics table or pics table
            picDB.insert(file_name, file_info.file_id, user_id, user_name)
            upPic.upload(file, file_name)
            bot.send_message(message.chat.id, txt)
            bot.send_message(message.chat.id, "Пришли еще картинку.\nДля отмены нажми /brake")
            del picDB
            if user_id == ADMIN_ID:
                bot.send_photo(PHOTO_CHANNEL, file_info.file_id)
            bot.register_next_step_handler(message, upload_photo)
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду картинку.\nДля отмены нажми /brake")
                bot.register_next_step_handler(message, upload_photo)    
        else:      
            bot.send_message(message.chat.id, "Это не то, но я жду картинку.\nДля отмены нажми /brake")
            bot.register_next_step_handler(message, upload_photo)


def upload_joke(message) -> None:
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in FILTER.COMMANDS:
                joke = message.text
                user_id = message.from_user.id 
                user_name = message.from_user.username 
                table = "adminJokes"
                userMessage = "Сохранил"
                if user_id != ADMIN_ID: 
                    table = "userJokes"
                    userMessage = "Добавлено на рассмотрение"
                    suggestions.new_suggest()
                jokeDB = utils.JokeDB(table)
                premium.new_upload_for_user(message)
                jokeDB.insert(joke, user_id, user_name)
                bot.send_message(message.chat.id, userMessage)
                if user_id == ADMIN_ID:
                    bot.send_message(JOKE_CHANNEL, joke)
                bot.send_message(message.chat.id, "Напиши анекдот.\nДля отмены нажми /brake")
                bot.register_next_step_handler(message, upload_joke)
            else:
               bot.send_message(message.chat.id, "Это не то, но я жду твой анекдот.\nДля отмены нажми /brake") 
               bot.register_next_step_handler(message, upload_joke)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Это не то, но я жду твой анекдот.\nДля отмены нажми /brake")
        bot.register_next_step_handler(message, upload_joke)


def upload_message_to_admin(message) -> None: 
    user_id = message.from_user.id
    user_name = message.from_user.username
    if message.content_type == "text":
        if message.text.lower() != "/brake":
            if message.text not in FILTER.COMMANDS:
                msgDB.insert(message.text, user_id, user_name)
                bot.send_message(message.chat.id, "Отправлено")
            else:
                bot.send_message(message.chat.id, "Это не то, но я жду твое сообщение.\nДля отмены нажми /brake")
                bot.register_next_step_handler(message, upload_message_to_admin)
        else:
            bot.send_message(message.chat.id, "Отменено")
    elif message.content_type == 'photo':
        upPic = utils.UploadPic(PATH.RECIEVED_PHOTOS)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file = bot.download_file(file_info.file_path)
        fileID = file_info.file_path.replace('photos/', '')
        upPic.upload(file, fileID)
        msgDB.new_file_id(fileID, user_id, user_name)
        if message.caption != None:
            caption = message.caption
            msgDB.update_msg_for_file_id(caption, fileID)
        bot.send_message(message.chat.id, "Отправил")
        del upPic
    else:
        bot.send_message(message.chat.id, "Это не то. Отправить можно только текст или картинку (необязательно с подписью). Напиши или отправь картинку.\nДля отмены нажми /brake")
        bot.register_next_step_handler(message, upload_message_to_admin)


def get_wct_photo(message) -> tuple[BufferedReader, str]:
    """
    WCT is "Which Caban (boar) you Today is"
    every day user changes his "board id"
    if user in one day, when he used function in bot, will use wct again, wct give the same "boar id"
    """
    
    user_id = message.from_user.id 

    premium.check_premium_is_over(message)
    db = premium.choice_DB_by_premium(user_id)
    if funcs.new_day(user_id):
        funcs.new_wct(user_id, db)

    boarID = userDB.get_wct_for_user(user_id)
    boar = db.get_record(boarID)
    achievements.check_new_boar(message, boar)
    caption = translate_category(BoarsCategories.get_boar_category(boar))

    return open(PATH.WCT + boar, 'rb'), caption


