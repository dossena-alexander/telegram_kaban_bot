import random
from datetime import date
from header import userDB
from config import LIMIT


def new_wct(userID, db) -> None:
    day = actual_day()
    userDB.set_previous_day(day, userID)
    boarID = random.randint(0, db.get_records_count() - 1)
    userDB.set_wct_for_user(userID, boarID)


def actual_day() -> int:
    now = date.today()
    actual_day = now.day
    return actual_day


def new_day(userID) -> bool:
    day = actual_day()
    previous_day = userDB.get_previous_day(userID)
    if day == previous_day:
        return False
    return True


def check_upload_day(user_id: int) -> bool:
    now_day = actual_day()
    upload_day = userDB.get_upload_day(user_id)
    if now_day == upload_day:
        return False
    return True


def new_upload_day(user_id: int) -> None:
    day = actual_day()
    userDB.update_upload_day(user_id, day)


def limit_reached(type: str, user_id: int) -> bool:
    """Available types: photo_upload, joke_upload, admin_msg

    Args:
        type (str): Type is column used to get uploads count
        user_id (int): TG id of user

    Returns:
        bool: True if limit reached
    """
    if type == 'photo_upload':
        limit = LIMIT.PHOTO
    elif type == 'joke_upload':
        limit = LIMIT.JOKE
    elif type == 'admin_msg':
        limit = LIMIT.MESSAGE
    count = userDB.get_upload_count(type, user_id)
    if count >= limit:
        return True
    return False