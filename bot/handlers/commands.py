from header import utils, bot, helpMenu, userDB, suggestions, adminMenu, userMenu, adminPicDB, adminJokeDB
from config import ADMIN_ID, KEYS, BOT_MESSAGE


def start(message):
    keyboard = utils.ReplyKeyboard()
    keyboard.set_keyboard(KEYS.START)
    bot.send_message(message.chat.id, "Вечер в хату, кабан {0.first_name}!"
        .format(message.from_user, bot.get_me()), reply_markup=keyboard.get())


def auth(message):
    userID = message.from_user.id
    if userID == ADMIN_ID:
        admin(message)
    else:
        usersList = userDB.getUsersList()
        if userID not in usersList:
            userDB.addUser(userID)
        user(message)


def help(message):
    helpMenu.setMsg(BOT_MESSAGE.HELP(photo_count = adminPicDB.getRecCount(), joke_count = adminJokeDB.getRecCount()))
    bot.send_message(message.chat.id, helpMenu.getMsg(), parse_mode="html")


def admin(message):
    if suggestions.exist():
        adminMenu.setMsg(suggestions.getMsg())
    else:
        adminMenu.setMsg("Админ меню")
    bot.send_message(message.chat.id, adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard(), parse_mode="html")


def user(message):
    bot.send_message(message.chat.id, userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard())
