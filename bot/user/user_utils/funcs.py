from header import date, random
from header import userDB


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
