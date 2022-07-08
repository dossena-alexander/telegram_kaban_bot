from header import adminPicDB, random, bot, utils, suggestions
from config import PATH, ADMIN_ID
from user import premiumProcess


def photoWorker(message): 
    if message.chat.type == 'private':
        if message.media_group_id != None: # able to save not only one pic
            bot.send_message(message.chat.id, "Я могу сохранить только одну картинку")
        else:
            id = message.from_user.id
            picDB = utils.PicDB("accPics")
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            if id == ADMIN_ID: 
                upPic = utils.UploadPic(PATH.PHOTOS)
                txt = "Сохранил"
                premiumProcess(message)
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
            del picDB