import telebot, random
from datetime import date
import shutil, os

from config import *
import utils


#========================INSTANCE===================================

bot = telebot.TeleBot(token=API_TOKEN)

userDB = utils.UserDB()
boarDB = utils.BoarDB()
premiumBoarDB = utils.PremiumBoarDB()
boarsCategories = utils.BoarsCategories()
msgDB = utils.MsgDB()

adminJokeDB = utils.JokeDB(table = "adminJokes")
adminPicDB = utils.PicDB(table = "accPics")

userPicDB = utils.PicDB(table = "pics")
userJokeDB = utils.JokeDB(table = "userJokes")

# records counter that`s used to see DB records in admin menu
class mesg():
    count = 0

suggestions = utils.suggestions()

#========================MENU===================================

adminMenu = utils.Menu()
userMenu = utils.Menu()
helpMenu = utils.Menu()
userSubMenu = utils.Menu()

#========================MENU_SET-UP===================================

adminMenu.set_message(BOT_MESSAGE.ADMIN)
adminMenu.set_inline_keyboard(KEYS.ADMIN)

userMenu.set_message(BOT_MESSAGE.USER)
userMenu.set_inline_keyboard(KEYS.USER)

userSubMenu.set_message(BOT_MESSAGE.USER_SUB_MENU)

helpMenu.set_message( BOT_MESSAGE.HELP(photo_count = adminPicDB.get_records_count(), 
                                       joke_count = adminJokeDB.get_records_count()) )