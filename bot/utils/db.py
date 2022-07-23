# from multiprocessing import Lock
from nis import cat
import sqlite3
import threading # thread_lock for DB cursor
import datetime
from unicodedata import category # needs to get now day
from config import PATH, PREMIUM_LIMIT
from utils.logger import log


lock = threading.Lock()

#      DB structure
# 
#      +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#      |TABLES         |COLUMNS                                          |
#      |===============|=================================================|
#      |accPics--------|-------------------------------------------------|
#      |               |fileID: |                                        |
#      |               |STRING  |                                        |
#      |pics-----------|-------------------------------------------------|
#      |               |fileID: |                                        |
#      |               |STRING  |                                        |
#      |adminJokes-----|-------------------------------------------------|
#      |               |joke:   |                                        |
#      |               |STRING  |                                        |
#      |userJokes------|-------------------------------------------------|
#      |               |joke:   |                                        |
#      |               |STRING  |                                        |
#      |boarsID--------|-------------------------------------------------|
#      |               |ID:     |                                        |
#      |               |STRING  |                                        |
#      |premiumBoarsID-|-------------------------------------------------|
#      |               |ID:     |                                        |
#      |               |STRING  |                                        |
#      |msgs-----------|-------------------------------------------------|
#      |               |msg:    |fileID:|                                |
#      |               |STRING  |STRING |                                |
#      |users------------------------------------------------------------|
#      |               |userID: |wctID: |prevDay: |status_premium: |uploadCount:|
#      |               |INTEGER |STRING |INTEGER  |INTEGER  |INTEGER     |
#      |vk_users-------|-------------------------------------------------|
#      |               |userID: |wctID: |prevDay: |                      |
#      |               |INTEGER |STRING |INTEGER  |                      |
#      +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+


def lock_thread(func):
    def _wrapper(self, *args, **kwargs):
        try:
            lock.acquire(True)
            return func(self, *args, **kwargs)
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()
    return _wrapper



class DB():
    def __init__(self) -> None:
        self._bd = sqlite3.connect(PATH.DB, check_same_thread=False)
        self._bd_cursor = self._bd.cursor()
        self._table = ''
        self._column = ''


    @lock_thread
    def delete_record(self, record: str) -> None:
        self._bd_cursor.execute( f'DELETE FROM {self._table} WHERE {self._column}=?', (record, ) )
        self._bd.commit()


    @lock_thread
    def new_record(self, record: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}) VALUES (?)', (record, ) ) 
        self._bd.commit()


    @lock_thread
    def hasRecords(self) -> bool:
        info = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        record = self._bd_cursor.fetchall()
        if len(record) == 0 or len(record) is None: 
            return False
        return True


    @lock_thread
    def get_records_count(self) -> int:
        info = self._bd_cursor.execute(f"SELECT * FROM {self._table}")
        rows = self._bd_cursor.fetchall()
        length = len(rows)
        return length


    @lock_thread
    def get_record(self, row: int) -> str:
        info = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        record = self._bd_cursor.fetchall()[row][0]
        return record

    
    def get_table(self) -> str:
        return self._table


    def get_column(self) -> str:
        return self._column

    
    def set_table(self, table_name: str) -> None:
        setattr(self, "_table", table_name)

    
    def set_column(self, column_name: str) -> None:
        setattr(self, "_col", column_name)




class UserDB(DB):
    def __init__(self, table = "users", column = "userID") -> None:
        super().__init__()
        self._table = table
        self._column = column


    @lock_thread
    def get_users_list(self) -> list[int]:
        info = self._bd_cursor.execute(f'SELECT {self._column} FROM {self._table}')
        records = self._bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        return records_listed


    @lock_thread
    def get_wct_for_user(self, userID: int) -> str:
        info = self._bd_cursor.execute(f'SELECT wctID FROM {self._table} WHERE {self._column}={userID}')
        return self._bd_cursor.fetchall()[0][0] # list > tuple > string


    @lock_thread
    def set_wct_for_user(self, userID: int, boarID: str) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET wctID = {boarID} WHERE {self._column}={userID}')
        self._bd.commit()


    @lock_thread    
    def get_previous_day(self, userID: int) -> int:
        info = self._bd_cursor.execute(f'SELECT prevDay FROM {self._table} WHERE {self._column}={userID}')
        record = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        return record
    
    @lock_thread
    def set_previous_day(self, day: int, userID: int) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET prevDay = {day} WHERE {self._column}={userID}')
        self._bd.commit()


    @lock_thread
    def add_user(self, userID: int) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}) VALUES (?)', (userID, ) )
        self._bd.commit()


    @lock_thread
    def is_premium(self, userID: int) -> bool:
        info = self._bd_cursor.execute(f'SELECT status_premium FROM {self._table} WHERE {self._column}={userID}')
        status_premium = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        if status_premium == 0:
            return False
        else:
            return True


    @lock_thread
    def activate_premium(self, userID: int, day: int) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET status_premium = 1 WHERE {self._column}={userID}')
        self._bd_cursor.execute(f'UPDATE {self._table} SET premiumDay = {day} WHERE {self._column}={userID}')
        self._bd.commit()


    @lock_thread
    def disactivate_premium(self, userID: int) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET status_premium = 0 WHERE {self._column}={userID}')
        self._bd.commit()


    @lock_thread
    def new_upload(self, userID: int) -> None:
        count = self.get_uploads_count(userID) + 1
        self._bd_cursor.execute(f'UPDATE {self._table} SET uploadCount = {count} WHERE {self._column}={userID}')
        self._bd.commit()


    def get_uploads_count(self, userID: int) -> int:
        try:
            log.error("МОДУЛЬ БЕЗ БЛОКИРОВКИ ПОТОКА")
            info = self._bd_cursor.execute(f'SELECT uploadCount FROM {self._table} WHERE {self._column}={userID}')
            uploads_count = self._bd_cursor.fetchall()[0][0] # list > tuple > string
            return uploads_count
        except Exception as e:
            log.error(e)
            print(e)


    @lock_thread
    def uploads_limit_reached(self, userID: int) -> bool:
        info = self._bd_cursor.execute(f'SELECT uploadCount FROM {self._table} WHERE {self._column}={userID}')
        uploads_count = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        if uploads_count >= PREMIUM_LIMIT.UPLOADS_COUNT:
            return True
        else:
            return False


    @lock_thread
    def delete_uploads_count(self, userID: int) -> None:
        count = self.get_uploads_count(userID)
        self._bd_cursor.execute(f'UPDATE {self._table} SET uploadCount = 0 WHERE {self._column}={userID}')
        self._bd.commit()


    @lock_thread
    def get_premium_turned_on_day(self, userID: int) -> int:
        self._bd_cursor.execute(f'SELECT premiumDay FROM {self._table} WHERE {self._column}={userID}')
        day = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        return day


    @lock_thread
    def user_unlocked_new_boar(self, userID: int, boar_category: str, boar: str) -> bool:
        self._bd_cursor.execute(f'SELECT {boar_category} FROM {self._table} WHERE {self._column}={userID}')
        boars = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        if boars == None:
            return True
        if boar in boars:
            return False
        return True


    def _all_boars(self, userID: int, boar_category: str) -> str:
        self._bd_cursor.execute(f'SELECT {boar_category} FROM {self._table} WHERE {self._column}={userID}')
        boars = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        return boars


    @lock_thread
    def get_user_boars(self, userID: int, boar_category: str) -> str:
        return self._all_boars(userID, boar_category)


    @lock_thread
    def new_boar_for_user(self, userID: int, boar: str, boar_category: str) -> None:
        new_boar = f"{self._all_boars(userID, boar_category)}, {boar}"
        self._bd_cursor.execute(f'UPDATE {self._table} SET {boar_category} = \'{new_boar}\' WHERE {self._column}={userID}')
        self._bd.commit()



class JokeDB(DB):
    def __init__(self, table: str) -> None:
        super().__init__()
        self._table = table
        self._column = 'joke'




class MsgDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "msgs"
        self._column = 'msg'


    @lock_thread
    def get_file_id(self, row: int) -> str:
        info = self._bd_cursor.execute(f'SELECT fileID FROM {self._table}')
        record = self._bd_cursor.fetchall()[row]
        fileID = record[0]
        return fileID


    @lock_thread
    def delete_msg_and_file_id(self, row: int) -> None:
        info = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        rec = self._bd_cursor.fetchall()[row]
        msg = rec[0]
        fileID = rec[1]
        self._bd_cursor.execute( f'DELETE FROM {self._table} WHERE msg=? OR fileID=?', (msg, fileID) )
        self._bd.commit()


    @lock_thread
    def msg_has_file_id(self, row: int) -> bool:
        info = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        record = self._bd_cursor.fetchall()[row]
        if record[1] == None:
            return False
        else:
            return True


    # new record with file id of photo sent to admin
    @lock_thread
    def new_file_id(self, record: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} (fileID) VALUES (?)', (record, ) ) 
        self._bd.commit()


    @lock_thread
    # new record with caption below photo sent to admin
    def insert_msg_for_file_id(self, msg: str, fileID: str) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET msg=\'{msg}\' WHERE fileID=\'{fileID}\'')
        self._bd.commit()




class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self._table = table
        self._column = 'fileID'
    



class BoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "boarsID"
        self._column = "ID"




class PremiumBoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "premiumBoarsID"
        self._column = "ID"




class BoarsCategories(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "Categories"


    def _get_record_from_column(self, column: str, row: int) -> str:
        info = self._bd_cursor.execute(f'SELECT {column} FROM {self._table}')
        return self._bd_cursor.fetchall()[row][0]


    def _get_columns_names(self):
        cursor = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        columns_names = list(map(lambda x: x[0], cursor.description))
        return columns_names


    @lock_thread
    def get_all_categories(self):
        return self._get_columns_names()


    @lock_thread
    def get_boars_of_category(self, category: str) -> list[str]:
        self._bd_cursor.execute(f'SELECT {category} FROM {self._table}')
        boars = self._bd_cursor.fetchall()
        boars_listed = [boar[0] for boar in boars]
        return boars_listed


    def get_boar_category(self, boarID: str) -> str:
        columns = self._get_columns_names()
        for column in columns:
            boars = self.get_boars_of_category(column)
            if boarID in boars:
                return column


    @lock_thread
    def new_boar(self, boar_category: str, boar: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({boar_category}) VALUES (?)', (boar, ) ) 
        self._bd.commit()




class Statistics(DB):
    def __init__(self) -> None:
        super().__init__()
        self.b    = BoarDB()
        self.p_b  = PremiumBoarDB()
        self.u    = UserDB()
        self.vk_u = UserDB("vk_users", "vk_id")
        self.j    = JokeDB("adminJokes")
        self.p    = PicDB("accPics")


    def get(self) -> str:
        boars = self.b.get_records_count()
        premium_boars = self.p_b.get_records_count()
        users = self.u.get_records_count()
        vk_users = self.vk_u.get_records_count()
        jokes = self.j.get_records_count()
        photos = self.p.get_records_count()
        txt = (f"<b>Статистика</b>\n•Кабаны: <b>{boars}</b>\n•Премиум кабаны: {premium_boars}\n•Пользователи: <b>{users}</b>\n•ВК Пользователи: <b>{vk_users}</b>\n•Анекдоты: <b>{jokes}</b>\n•Картинки: <b>{photos}</b>")
        return txt




class suggestions():
    # when users upload photo or joke counter increases to the limit, then bot sends message to admin
    _limit = PREMIUM_LIMIT.UPLOADS_COUNT 
    _all_suggestions_counter = 0
    _upload_counter = 0
    _suggestions_notification = False
    _photo_suggestions = 0
    _jokes_suggestions = 0
    _messages_suggestions = 0


    def __init__(self) -> None:
        self._tables = {'pics': 'fileID', 'userJokes': 'joke', 'msgs': 'msg'}


    def exist(self) -> bool:
        suggestions_exist = False
        db = DB()

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


    def get_message(self) -> str:
        self._all_suggestions_counter = 0
        msg = ( "Админ меню.\n" +
                f"Картинок: {self._photo_suggestions}. " +
                f"Сообщений: {self._messages_suggestions}. " +
                f"Анекдотов: {self._jokes_suggestions}")

        return msg




class Achievements():
    _message: str


    def __init__(self, userID) -> None:
        super().__init__()
        self.boarsCategories = BoarsCategories()
        self._categories = self.boarsCategories.get_all_categories()
        self.count_achievements(userID)
        message = (
            f"<b>Открытые кабаны:</b>\n"+
            f" •Эмотивные: "            + f"<b><i>{self._categories[0]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Игровые: "              + f"<b><i>{self._categories[1]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Мировые: "              + f"<b><i>{self._categories[2]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Братья большие: "       + f"<b><i>{self._categories[3]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Братья меньшие: "       + f"<b><i>{self._categories[4]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Философские: "          + f"<b><i>{self._categories[5]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Легендарные: "          + f"<b><i>{self._categories[6]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Интересные персоны: "   + f"<b><i>{self._categories[7]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •С подвохом: "           + f"<b><i>{self._categories[8]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Высшие слои общества: " + f"<b><i>{self._categories[9]}%</i></b>\n"  +
            "----------------------------------------\n"                             +
            f" •Премиальные: "          + f"<b><i>{self._categories[10]}%</i></b>"
        )
        self._set_message(message)
        del self.boarsCategories


    def get_message(self) -> str:
        return self._message


    def _set_message(self, text: str) -> None:
        self._message = text


    def _listed_string(self, string: str) -> list[str]:
        return list(string)


    def _split_to_list(self, string: str) -> list[str]:
        if len(string) > 5: # do not contains "empty"
            return string.split(', ')
            
        return self._listed_string(string)


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
        userDB = UserDB()
        user_boars = userDB.get_user_boars(userID, column)
        del userDB
        if user_boars == "empty": 
            return 0
        user_boars_listed = self._split_to_list(user_boars)

        return self._check_achivement(user_boars_listed, column)


    def _set_categoria_count(self, userID: int, columns: list[str]) -> None:
        for column in columns:
            self._categories[columns.index(column)] = self._count_for_column(userID, column)


    def count_achievements(self, userID: int) -> None:
        self._set_categoria_count(userID, self._categories)




class PremiumMenu():
    _message: str


    def __init__(self, userID) -> None:
        self.userDB = UserDB()
        premium_status = self._get_status(userID)
        days = self._calculate_premium_days(userID)
        self._set_message(
            f"•Статус: {premium_status}" "\n" +
            f"•Дней: {days}"
        )
        del self.userDB


    def _get_status(self, userID: int) -> str:
        if self.userDB.is_premium(userID):
            return "<b>Активен</b>"
        return "<b>Не активен</b>"


    def _calculate_premium_days(self, userID) -> int:
        premium_toggled_on_day = self.userDB.get_premium_turned_on_day(userID)
        disactivate_day = premium_toggled_on_day + PREMIUM_LIMIT.DAYS
        date = datetime.date.today()
        day = date.day
        days_left = disactivate_day - day
        if days_left == 0:
            return "<b>0</b> <i>(завтра отключение)</i>"
        return f"<b>{abs(days_left)}</b>"


    def _set_message(self, text: str) -> None:
        self._message = text


    def get_message(self) -> str:
        return self._message


    def get_text_about() -> str:
        return ("<i>Что такое премиум?</i>" "\n" +
                    "Премиум это знак уникальности, что вы -- активный пользователь." "\n" +
                    "С помощью премиум можно получать уникальных кабанов, а чтобы получить премиум нужно:\n" +
                    "•<b>Загрузить в бота не менее 5-ти предложений.</b>\nЭто могут быть анекдоты, картинки, или все вместе.\n" +
                    "Бот автоматически поймет, что вы загрузили достаточно предложений и выдаст уникального кабана, о чем немедленно сообщит.\n" +
                    "Во время премиума счетчик загрузок работать не будет\n" +
                    "•Длится премиум <b>2 дня</b>"
        )
