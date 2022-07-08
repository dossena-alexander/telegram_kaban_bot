from header import adminPicDB, random, adminJokeDB, bot, shedule, utils, suggestions
from config import PATH, SHEDULE_SITE, ADMIN_ID
from user import getWct


def textWorker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        if suggestions.reachedLimit():
            bot.send_message(ADMIN_ID, f"Есть новые {suggestions.counter} предложений")
        bot.send_photo(message.chat.id, 
        open(PATH.PHOTOS + adminPicDB.getRecord(recNum=random.randint(0, adminPicDB.getRecCount() - 1)), "rb"))
    elif msg == "анекдот":
        if suggestions.reachedLimit():
            bot.send_message(ADMIN_ID, f"Есть новые {suggestions.counter} предложений")
        bot.send_message(message.chat.id, 
        adminJokeDB.getRecord(recNum=random.randint(0, adminJokeDB.getRecCount() - 1)))
    elif msg == "какой я кабан сегодня":
        if suggestions.reachedLimit():
            bot.send_message(ADMIN_ID, f"Есть новые {suggestions.counter} предложений")
        if getWct(message) != None:
            bot.send_photo(message.chat.id, getWct(message))
    elif msg == "расписание":
        key = utils.InlineKeyboard()
        key.addUrlButton("Сайт с заменами", SHEDULE_SITE)
        bot.send_photo(message.chat.id, shedule.getShedule(), shedule.currentDay(), reply_markup=key.get())


