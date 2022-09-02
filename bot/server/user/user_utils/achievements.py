from header import utils
from header import bot, userDB
from server.admin.admin_utils.statistics import Statistics


boarsCategories = utils.BoarsCategories()


class Achievements():
    _message: str


    def __init__(self, userID) -> None:
        self.boarsCategories = boarsCategories
        self._categories = self.boarsCategories.get_all_categories()
        self.count_achievements(userID)
        message = (
            f"<b>Открытые кабаны:</b>\n"+
            f" • Эмотивные: "            + f"<b><i>{self._categories[0]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Игровые: "              + f"<b><i>{self._categories[1]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Мировые: "              + f"<b><i>{self._categories[2]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Братья большие: "       + f"<b><i>{self._categories[3]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Братья меньшие: "       + f"<b><i>{self._categories[4]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Философские: "          + f"<b><i>{self._categories[5]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Легендарные: "          + f"<b><i>{self._categories[6]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Интересные персоны: "   + f"<b><i>{self._categories[7]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • С подвохом: "           + f"<b><i>{self._categories[8]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Высшие слои общества: " + f"<b><i>{self._categories[9]}%</i></b>\n"  +
            "----------------------------------------\n"                              +
            f" • Премиальные: "          + f"<b><i>{self._categories[10]}%</i></b>\n"   +
            "----------------------------------------\n"                              +
            f" • Субкультурные: "        + f"<b><i>{self._categories[11]}%</i></b>"
        )
        self._set_message(message)
        del self.boarsCategories

    def get_message(self) -> str:
        return self._message

    def _set_message(self, text: str) -> None:
        self._message = text

    def _split_to_list(self, string: str) -> list[str]:
        if len(string) > 5: # do not contains "empty"
            return string.split(', ')

        return list(string)

    def _delete_none_from_list(self, with_none_list: list[str]) -> list[str]:
        not_none_list = []
        for string in with_none_list:
            if string != None:
                not_none_list.append(string)

        return not_none_list

    def _transform_to_percent(self, count: int, boar_category: str) -> int:
        boars_in_category = self.boarsCategories.get_boars_of_category(boar_category)
        boars_length_in_category = len(self._delete_none_from_list(boars_in_category))

        return count / boars_length_in_category * 100

    def _check_achivement(self, boars: list[str], category: str) -> str:
        all_boars_in_category = self.boarsCategories.get_boars_of_category(category) # -> list
        count = 0
        for boar in boars:
            if boar in all_boars_in_category:
                count += 1

        count = self._transform_to_percent(count, category)
        return "{:2.2f}".format(count)

    def _count_for_column(self, userID: int, column: str) -> int:
        user_boars = userDB.get_user_boars(userID, column)
        if user_boars == "empty": 
            return 0

        user_boars_listed = self._split_to_list(user_boars)
        return self._check_achivement(user_boars_listed, column)

    def _set_categoria_count(self, userID: int, columns: list[str]) -> None:
        for column in columns:
            self._categories[columns.index(column)] = self._count_for_column(userID, column)

    def count_achievements(self, userID: int) -> None:
        self._set_categoria_count(userID, self._categories)


def translate_category(category: str) -> str:
    """Translate boar category to russian

    Args:
        category str: Category in english

    Returns:
        str: Category in russian
    """
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
    elif category == "sub_culture":
        return "Субкультурные"


def _new_boar(message, userID, boar_category, boar):
    translated_category = translate_category(boar_category)
    bot.send_message(message.chat.id, f"Ты открыл нового кабана из категории <i>{translated_category}</i>", parse_mode="html")
    userDB.new_boar_for_user(userID, boar, boar_category)


def _record_boar() -> None:
    db = Statistics()
    db.update_boar()
    del db


def check_new_boar(message, boar):
    userID = message.from_user.id
    category = boarsCategories.get_boar_category(boar)
    if userDB.user_unlocked_new_boar(userID, category, boar):
        _new_boar(message, userID, category, boar)
        _record_boar()

