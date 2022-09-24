from datetime import date
from header import utils
from header import bot, userDB
from config import PREMIUM_LIMIT
from server.user.user_utils import funcs


boarDB = utils.BoarDB()
premiumBoarDB = utils.PremiumBoarDB()


class PremiumMenu():
    _message: str
    _premium_status: str
    _days_gone: str

    def __init__(self, userID) -> None:
        self.userDB = userDB
        self._premium_status = self._get_status(userID)
        self._days_gone = self._calculate_premium_days(userID)
        self._set_message(
            f"•Статус: {self._premium_status}" "\n" +
            f"•Дней: {self._days_gone}"
        )
        del self.userDB

    def _get_status(self, userID: int) -> str:
        if self.userDB.is_premium(userID):
            return "<b>Активен</b>"
        return "<b>Не активен</b>"

    def _calculate_premium_days(self, userID) -> int:
        premium_turned_day = self.userDB.get_premium_turned_day(userID)
        disactivate_day = premium_turned_day + PREMIUM_LIMIT.DAYS
        now = date.today()
        day = now.day
        days_left = disactivate_day - day
        if days_left == 0:
            return "<b>0</b> <i>(завтра отключение)</i>"
        return f"<b>{abs(days_left)}</b>"

    def _set_message(self, text: str) -> None:
        self._message = text

    def get_message(self) -> str:
        return self._message

    def get_text_about() -> str:
        return ("<i>Что такое премиум?</i>" "\n" 
                + "Премиум это знак уникальности, что вы -- активный пользователь." "\n" 
                + "С помощью премиум можно получать уникальных кабанов, а чтобы получить премиум нужно:\n" 
                + "• <b>Загрузить в бота не менее 5-ти предложений.</b>\nЭто могут быть анекдоты, картинки, или все вместе.\n" 
                + "Бот автоматически поймет, что вы загрузили достаточно предложений и выдаст уникального кабана, о чем немедленно сообщит.\n" 
                + "Во время премиума счетчик загрузок работать не будет\n" 
                + " •Длится премиум <b>2 дня</b>"
            )

    @property
    def status(self) -> str:
        return self._premium_status

    @property
    def days(self) -> int:
        return self._days_gone


def choice_DB_by_premium(user_id: int):
    db = boarDB
    if userDB.is_premium(user_id):
        db = premiumBoarDB
    return db


def check_premium_is_over(message) -> None:
    user_id = message.from_user.id
    if userDB.is_premium(user_id) and funcs.actual_day() - userDB.get_premium_turned_day(user_id) > PREMIUM_LIMIT.DAYS:
        userDB.disactivate_premium(user_id)
        funcs.new_wct(user_id, boarDB)
        bot.send_message(message.chat.id, "Истек срок премиума!\nКак получить премиум читай в /auth -> Премиум")


def new_upload_for_user(message) -> None:
    user_id = message.from_user.id
    if userDB.is_premium(user_id) == False:
        userDB.new_upload(user_id)
    check_upload_limit(message)


def check_upload_limit(message) -> None:
    user_id = message.from_user.id
    if userDB.uploads_limit_reached(user_id):
        userDB.activate_premium(user_id, funcs.actual_day())
        userDB.delete_uploads_count(user_id)
        funcs.new_wct(user_id, premiumBoarDB)
        bot.send_message(message.chat.id, "Поздравляю! Ты премиальный кабан!\nПроверь, нажми кнопку)")