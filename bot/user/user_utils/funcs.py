from header import bot, utils, userDB, date, random, boarDB, premiumBoarDB, boarsCategories
from header import PREMIUM_LIMIT


def new_wct(userID, db) -> None:
    day = _actual_day()
    userDB.set_previous_day(day, userID)
    boarID = random.randint(0, db.get_records_count() - 1)
    userDB.set_wct_for_user(userID, boarID)


def choice_DB_by_premium(userID) -> utils.DB:
    db = boarDB
    if userDB.is_premium(userID):
        db = premiumBoarDB
    return db


def _actual_day() -> int:
    now = date.today()
    actual_day = now.day
    return actual_day


def new_day(userID) -> bool:
    day = _actual_day()
    previous_day = userDB.get_previous_day(userID)
    if day == previous_day:
        return False
    return True


def _translate_category(category) -> str:
    if category == "emotions":
        return "Эмотивные"
    elif category == "game":
        return "Игровые"
    elif category == "world":
        return "Мировые"
    elif category == "big":
        return "Братья большие"
    elif category == "small":
        return "Братья меньшие"
    elif category == "phylosophy":
        return "Философские"
    elif category == "legend":
        return "Легендарные"
    elif category == "interesting":
        return "Интересные персоны"
    elif category == "trap":
        return "С подвохом"
    elif category == "upper_stratum":
        return "Высшие слои общества"
    elif category == "premium":
        return "Премиальные"


def _new_boar(message, userID, boar_category, boar):
    translated_category = _translate_category(boar_category)
    bot.send_message(message.chat.id, f"Ты открыл нового кабана из категории <i>{translated_category}</i>", parse_mode="html")
    userDB.new_boar_for_user(userID, boar, boar_category)


def check_new_boar(message, boar):
    userID = message.from_user.id
    category = boarsCategories.get_boar_category(boar)
    if userDB.user_unlocked_new_boar(userID, category, boar):
        _new_boar(message, userID, category, boar)


def premium_process(message):
    userID = message.from_user.id
    if userDB.is_premium(userID) and _actual_day() - userDB.get_premium_turned_on_day(userID) > PREMIUM_LIMIT.DAYS:
        userDB.disactivate_premium(userID)
        new_wct(userID, boarDB)
        bot.send_message(message.chat.id, "Истек срок премиума!\nКак получить премиум читай в /auth -> Премиум")


def new_upload_for_user(message):
    userID = message.from_user.id
    if userDB.is_premium(userID) == False:
        userDB.new_upload(userID)
    check_upload_limit(message, userID)


def check_upload_limit(message, userID):
    if userDB.uploads_limit_reached(userID):
        userDB.activate_premium(userID, _actual_day())
        userDB.delete_uploads_count(userID)
        new_wct(userID, premiumBoarDB)
        bot.send_message(message.chat.id, "Поздравляю! Ты премиальный кабан!\nПроверь, нажми кнопку)")