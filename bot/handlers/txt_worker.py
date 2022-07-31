from header import adminPicDB, random, adminJokeDB, bot
from config import PATH, ADMIN_ID
from admin.admin_utils import suggestions
from user.user_funcs import get_wct_photo


def reply_keyboard_worker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        _check_suggestions()
        _send_photo(message)
    elif msg == "анекдот":
        _check_suggestions()
        _send_joke(message)
    elif msg == "какой я кабан сегодня":
        _check_suggestions()
        _send_wct(message)


def _send_wct(message):
    if get_wct_photo(message) != None:
        bot.send_photo(message.chat.id, get_wct_photo(message))


def _send_joke(message):
    bot.send_message(message.chat.id, 
        adminJokeDB.get_record(row=random.randint(0, adminJokeDB.get_records_count() - 1)))


def _send_photo(message):
    bot.send_photo(message.chat.id, 
        open(PATH.PHOTOS + adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1)), "rb"))


def _check_suggestions():
    if suggestions.limit_reached():
        bot.send_message(ADMIN_ID, f"Есть новые {suggestions.all_suggestions} предложений")

