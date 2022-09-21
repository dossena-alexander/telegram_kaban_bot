import random
from header import bot, userDB, adminMenu, userMenu, adminPicDB, adminJokeDB
from config import ADMIN_ID, PATH
from server.admin.admin_utils.suggestions import Suggestions
import server.admin.admin_funcs as admin_funcs
from server.utils.ban import BannedDB
from server.user.user_funcs import get_wct_photo
from server.utils.keyboard import InlineKeyboard
from server.admin.admin_utils.statistics import Statistics
from server.utils.charts.collector import ClickCollector
from server.user.user_utils import Achievements


stats = Statistics()
jokeClickCollector = ClickCollector('joke_clicks')
photoClickCollector = ClickCollector('photo_clicks')
wctClickCollector = ClickCollector('wct_clicks')


def start(message):
    user_id = message.from_user.id
    usersList = userDB.get_users_list()
    if user_id not in usersList:
        userDB.add_user(user_id)

    see_manual = InlineKeyboard()
    see_manual.add_button('Посмотреть', 'USER_EXCURSUS')

    bot.send_message(message.chat.id, "Хрю хрю, кабан {0.first_name}!"
        .format(message.from_user, bot.get_me()))
    bot.send_message(message.chat.id, 'Обязательно посмотри мануал)', reply_markup=see_manual)


def ban(message):
    if message.from_user.id == ADMIN_ID:
        err = admin_funcs.ban_user(message)
        if err != None:
            bot.reply_to(message, err)
        else:
            bot.reply_to(message, "Забанил пользователя")


def unban(message):
    if message.from_user.id == ADMIN_ID:
        admin_funcs.unban_user(message)
        bot.reply_to(message, "Разбанил пользователя")


def banList(message):
    if message.from_user.id == ADMIN_ID:
        banDB = BannedDB()
        banList = banDB.get_users_idName_list()
        if not banList:
            bot.reply_to(message, "Забаненных пользователей нет")
        else:
            bot.send_message(message.chat.id, banList)


def auth(message):
    userID = message.from_user.id
    if userID == ADMIN_ID:
        admin(message)
    else:
        user(message)


def help(message):
    keyboard = InlineKeyboard()
    keyboard.add_button('Достижения', 'USER_EX_ACHIEVEMENTS')
    keyboard.add_button('Премиум', 'USER_EX_PREMIUM')
    keyboard.add_button('Сообщение админу', 'USER_EX_ADMIN_MSG')
    keyboard.add_button('Настройки', 'USER_EX_SETTINGS')
    keyboard.add_button('Команды', 'USER_EX_COMMANDS')
    photo = open(PATH.HELP+'user_menu/'+'default.png', 'rb')
    bot.send_photo(message.chat.id, photo, "Помощь по функциям бота", reply_markup=keyboard)


def admin(message):
    adminMenu.set_message("Админ меню")
    suggestions = Suggestions()
    if suggestions.exist():
        adminMenu.set_message(suggestions.get_message())
    bot.send_message(message.chat.id, adminMenu.message, reply_markup=adminMenu.get_inline_keyboard(), parse_mode="html")


def user(message):
    bot.send_message(message.chat.id, userMenu.message, reply_markup=userMenu.get_inline_keyboard())


def send_wct(message):
    check_suggestions()
    user_id = message.from_user.id
    users = userDB.get_users_list()

    if user_id != ADMIN_ID and user_id not in users:
        bot.send_message(message.chat.id, "Ты не зарегистрировался. Нажми /auth, чтобы зарегистрироваться", reply_to_message_id=message.message_id)
        return None
    else:
        stats.update_wct()
        wctClickCollector.new_by_db()
        boar, caption = get_wct_photo(message)
        bot.send_photo(message.chat.id, boar, reply_to_message_id=message.message_id, caption=caption)


def send_joke(message):
    check_suggestions()
    stats.update_joke()
    jokeClickCollector.new_by_db()
    bot.send_message(message.chat.id, 
        adminJokeDB.get_record(row=random.randint(0, adminJokeDB.get_records_count() - 1)), 
        parse_mode='html')


def send_photo(message): # by file_id
    check_suggestions()
    stats.update_photo()
    photoClickCollector.new_by_db()
    bot.send_photo(message.chat.id, 
        adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1), col=1))


def check_suggestions():
    suggestions = Suggestions()
    if suggestions.limit_reached():
        bot.send_message(ADMIN_ID, f"Есть новые {suggestions.all_suggestions} предложений")


def achieve_boars(message):
    achievements = Achievements(message.from_user.id)
    bot.send_message(message.chat.id, achievements.get_message(), parse_mode="html")