from header import adminPicDB, random, adminJokeDB, bot, shedule, utils, config
from user.user_funcs import getWct


def textWorker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        bot.send_photo(message.chat.id, 
        open(config.photos_path + adminPicDB.getPicID(recNum=random.randint(0, adminPicDB.getRecCount() - 1)), "rb"))
    elif msg == "анекдот":
        bot.send_message(message.chat.id, 
        adminJokeDB.getRecord(recNum=random.randint(0, adminJokeDB.getRecCount() - 1)))
    elif msg == "какой я кабан сегодня":
        if getWct(message) != None:
            bot.send_photo(message.chat.id, getWct(message))
    elif msg == "расписание":
        key = utils.InlineKeyboard()
        key.addUrlButton("Сайт с заменами", "http://www.lmk-lipetsk.ru/main_razdel/shedule/index.php")
        bot.send_photo(message.chat.id, open(shedule.getShedule(), 'rb'), shedule.currentDay(), reply_markup=key.get())
