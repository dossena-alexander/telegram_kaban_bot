from header import adminPicDB, random, adminJokeDB, bot, userDB
from config import PATH, ADMIN_ID
from admin.admin_utils.suggestions import Suggestions
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
    user_id = message.from_user.id
    users = userDB.get_users_list()

    if user_id != ADMIN_ID and user_id not in users:
        bot.send_message(message.chat.id, "Ты не зарегистрировался. Нажми /auth, чтобы зарегистрироваться")
        return None
    else:
        bot.send_photo(message.chat.id, get_wct_photo(message))


def _send_joke(message):
    bot.send_message(message.chat.id, 
        adminJokeDB.get_record(row=random.randint(0, adminJokeDB.get_records_count() - 1)))


# def _send_photo(message): # by file_name in DB
#     bot.send_photo(message.chat.id, 
#         open(PATH.PHOTOS + adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1)), "rb"))


def _send_photo(message): # by file_id
    bot.send_photo(message.chat.id, 
        adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1), col=1))


def _check_suggestions():
    suggestions = Suggestions()
    if suggestions.limit_reached():
        bot.send_message(ADMIN_ID, f"Есть новые {suggestions.all_suggestions} предложений")

