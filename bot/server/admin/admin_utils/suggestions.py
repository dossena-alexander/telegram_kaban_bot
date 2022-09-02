from config import PREMIUM_LIMIT
from header import utils


class Suggestions():
    _suggestions_notification = False
    
    # when users upload photo or joke counter increases to the limit, then bot sends message to admin
    _limit = PREMIUM_LIMIT.UPLOADS_COUNT 
    _upload_counter = 0

    _all_suggestions_counter = 0
    _photo_suggestions = 0
    _jokes_suggestions = 0
    _messages_suggestions = 0


    def __init__(self) -> None:
        self._tables = {'pics': 'fileID', 
                        'userJokes': 'joke', 
                        'msgs': 'msg'}
                        
    def get_message(self) -> str:
        self._all_suggestions_counter = 0
        msg = ( "Админ меню.\n" +
                f"Картинок: {self._photo_suggestions}. " +
                f"Сообщений: {self._messages_suggestions}. " +
                f"Анекдотов: {self._jokes_suggestions}")
        return msg

    def exist(self) -> bool:
        suggestions_exist = False
        db = utils.DB()

        for table, column in self._tables.items():
            db.set_table(table)
            db.set_column(column)
            count = db.get_records_count()
            if count == None: count = 0
            if count > 0:
                suggestions_exist = True
                if table == "pics":
                    self._photo_suggestions = count
                elif table == "userJokes":
                    self._jokes_suggestions = count
                elif table == "msgs":
                    self._messages_suggestions = count
        del db
        return suggestions_exist

    def _check_limit(self) -> bool:
        if self._upload_counter >= self._limit:
            return True
        return False

    def limit_reached(self) -> bool:
        if self._suggestions_notification:
            self._suggestions_notification = False
            return True
        return False

    @property
    def all_suggestions(self):
        return self._all_suggestions_counter
    
    def new_suggest(self) -> None:
        self._upload_counter += 1
        self._all_suggestions_counter += 1
        if self._check_limit():
            self._suggestions_notification = True
            self._upload_counter = 0