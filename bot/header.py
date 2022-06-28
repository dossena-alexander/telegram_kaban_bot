import telebot, random
from datetime import date
import config
import utils
import shutil, os

#========================INSTANCE===================================

bot = telebot.TeleBot(token=config.token)

userDB = utils.UserDB()
boarDB = utils.BoarDB()
msgDB = utils.MsgDB()

adminJokeDB = utils.JokeDB("adminJokes")
adminPicDB = utils.PicDB("accPics")

userPicDB = utils.PicDB("pics")
userJokeDB = utils.JokeDB("userJokes")

msgCounter = 0 # records counter that`s used to see user msgs in admin menu
new_suggestions = utils.new_suggestions()
shedule = utils.Shedule()

#========================MENU===================================

adminMenu = utils.Menu()
userMenu = utils.Menu()
helpMenu = utils.Menu()
userSubMenu = utils.Menu()

#========================MENU_SET-UP===================================

userSubMenu.setMsg(config.userSubMenuMsg)
helpMenu.setMsg(config.helpMsg)

adminMenu.setMsg(config.adminMsg)
adminMenu.setInlineKeyboard(config.adminKeys)
adminMenu.rowInlineKeyboard()

userMenu.setMsg(config.userMsg)
userMenu.setInlineKeyboard(config.userKeys)
userMenu.rowInlineKeyboard()
