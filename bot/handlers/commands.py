from header import utils, bot, config, helpMenu, userDB, new_suggestions, adminMenu, userMenu


def start(message):
    keyboard = utils.ReplyKeyboard()
    keyboard.add(config.startKeys)
    keyboard.autoRow()
    bot.send_message(message.chat.id, "Вечер в хату, кабан {0.first_name}!"
        .format(message.from_user, bot.get_me()), reply_markup=keyboard.get())


def auth(message):
    userID = message.from_user.id
    if userID == config.adminID:
        admin(message)
    else:
        usersList = userDB.getUsersList()
        if userID not in usersList:
            userDB.addUser(userID)
        user(message)


def help(message):
    bot.send_message(message.chat.id, helpMenu.getMsg(), parse_mode="html")


def admin(message):
    if new_suggestions.exist():
        adminMenu.setMsg(new_suggestions.getMsg())
    else:
        adminMenu.setMsg("Админ меню")
    bot.send_message(message.chat.id, adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard(), parse_mode="html")


def user(message):
    bot.send_message(message.chat.id, userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard()) 
