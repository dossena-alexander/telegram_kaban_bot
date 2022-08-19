from config import *
from server import utils


#========================INSTANCE===================================

bot = utils.ban.Ban_telebot(token=API_TOKEN)


userDB = utils.UserDB()
msgDB = utils.MsgDB()

adminJokeDB = utils.JokeDB(table = "adminJokes")
adminPicDB = utils.PicDB(table = "accPics")

userJokeDB = utils.JokeDB(table = "userJokes")
userPicDB = utils.PicDB(table = "pics")

# records counter that`s used to see DB records in admin menu
class mesg():
    count = 0

#========================MENU===================================

adminMenu = utils.Menu()
userMenu = utils.Menu()
helpMenu = utils.Menu()
user_translate_menu = utils.Menu()

#========================MENU_SET-UP===================================

adminMenu.set_message(BOT_MESSAGE.ADMIN)
adminMenu.set_inline_keyboard(KEYS.ADMIN)

userMenu.set_message(BOT_MESSAGE.USER)
userMenu.set_inline_keyboard(KEYS.USER)

user_translate_menu.set_message(BOT_MESSAGE.USER_SUB_MENU)