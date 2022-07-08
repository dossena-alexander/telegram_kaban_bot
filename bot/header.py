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
msgDB = utils.MsgDB()

adminJokeDB = utils.JokeDB("adminJokes")
adminPicDB = utils.PicDB("accPics")

userPicDB = utils.PicDB("pics")
userJokeDB = utils.JokeDB("userJokes")

# records counter that`s used to see DB records in admin menu
class mesg():
    count = 0

suggestions = utils.suggestions()
shedule = utils.Shedule()

#========================MENU===================================

adminMenu = utils.Menu()
userMenu = utils.Menu()
helpMenu = utils.Menu()
userSubMenu = utils.Menu()

#========================MENU_SET-UP===================================

adminMenu.setMsg(BOT_MESSAGE.ADMIN)
adminMenu.setInlineKeyboard(KEYS.ADMIN)

userMenu.setMsg(BOT_MESSAGE.USER)
userMenu.setInlineKeyboard(KEYS.USER)

userSubMenu.setMsg(BOT_MESSAGE.USER_SUB_MENU)

helpMenu.setMsg(BOT_MESSAGE.HELP(photo_count = adminPicDB.getRecCount(), joke_count = adminJokeDB.getRecCount()))