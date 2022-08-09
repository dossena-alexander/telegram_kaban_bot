from header import adminPicDB, userPicDB, bot, utils
from config import PATH, ADMIN_ID
from admin.admin_utils.suggestions import Suggestions
from user.user_utils import new_upload_for_user


suggestions = Suggestions()


def upload_photo_in_private_chat(message): 
    if message.chat.type == 'private':
        if message.media_group_id != None: # able to save not only one pic
            bot.send_message(message.chat.id, "Я могу сохранить только одну картинку")
        else:
            user_id = message.from_user.id
            picDB = adminPicDB
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            if user_id == ADMIN_ID: 
                upPic = utils.UploadPic(PATH.PHOTOS)
                txt = "Сохранил"
            else:
                upPic = utils.UploadPic(PATH.RECIEVED_PHOTOS)
                txt = "Добавлено на рассмотрение"
                picDB = userPicDB
                suggestions.new_suggest()
            new_upload_for_user(message)
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            file = bot.download_file(file_info.file_path)
            file_name = file_info.file_path.replace('photos/', '')
            # saving photo id to DB of pics, either accepted pics table or pics table
            picDB.new_record(file_name)
            upPic.upload(file, file_name)
            bot.send_message(message.chat.id, txt)
            del picDB