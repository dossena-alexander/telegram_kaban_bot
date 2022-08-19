import sqlite3
import threading # thread_lock for DB cursor

from config import PATH, PREMIUM_LIMIT
from server.utils.logger import log


lock = threading.Lock()

#      DB structure
# 
#      +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#      |TABLES         |COLUMNS                                                   |
#      |===============|==========================================================|
#      |accPics--------|----------------------------------------------------------|
#      |               |fileID: |                                                 |
#      |               |STRING  |                                                 |
#      |pics-----------|----------------------------------------------------------|
#      |               |fileID: |                                                 |
#      |               |STRING  |                                                 |
#      |adminJokes-----|----------------------------------------------------------|
#      |               |joke:   |                                                 |
#      |               |STRING  |                                                 |
#      |userJokes------|----------------------------------------------------------|
#      |               |joke:   |                                                 |
#      |               |STRING  |                                                 |
#      |boarsID--------|----------------------------------------------------------|
#      |               |ID:     |                                                 |
#      |               |STRING  |                                                 |
#      |premiumBoarsID-|----------------------------------------------------------|
#      |               |ID:     |                                                 |
#      |               |STRING  |                                                 |
#      |msgs-----------|----------------------------------------------------------|
#      |               |msg:    |fileID:|                                         |
#      |               |STRING  |STRING |                                         |
#      |users---------------------------------------------------------------------|
#      |               |userID: |wctID: |prevDay: |status_premium:   |uploadCount:|
#      |               |INTEGER |STRING |INTEGER  |INTEGER  |INTEGER |INTEGER     |
#      |vk_users-------|----------------------------------------------------------|
#      |               |userID: |wctID: |prevDay: |                               |
#      |               |INTEGER |STRING |INTEGER  |                               |
#      +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+


def lock_thread(func):
    def _wrapper(self, *args, **kwargs):
        try:
            lock.acquire(True)
            return func(self, *args, **kwargs)
        except Exception as e:
            log.error(f"{func}: {e}")
            print(f"{func}: {e}")
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
    def get_record(self, row: int, col: int = 0) -> str:
        info = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        record = self._bd_cursor.fetchall()[row][col]
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
        fileID = record[1]
        if fileID == None:
            return False
        return True

    # new record with file id of photo sent to admin
    @lock_thread
    def new_file_id(self, record: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} (fileID) VALUES (?)', (record, ) ) 
        self._bd.commit()

    # new record with caption below photo sent to admin
    @lock_thread
    def insert_msg_for_file_id(self, msg: str, fileID: str) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET msg=\'{msg}\' WHERE fileID=\'{fileID}\'')
        self._bd.commit()


class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self._table = table
        self._column = 'fileID'
        self._column_2 = 'tg_id'


    @lock_thread
    def insert(self, file_name: str, file_id: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}, {self._column_2}) VALUES (?, ?)', (file_name, file_id) ) 
        self._bd.commit()


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
        self.set_table('stats')

    def get(self) -> str:
        self.b    = BoarDB()
        self.p_b  = PremiumBoarDB()
        self.u    = UserDB()
        self.vk_u = UserDB("vk_users", "vk_id")
        self.j    = JokeDB("adminJokes")
        self.p    = PicDB("accPics")

        boars = self.b.get_records_count()
        premium_boars = self.p_b.get_records_count()
        users = self.u.get_records_count()
        vk_users = self.vk_u.get_records_count()
        jokes = self.j.get_records_count()
        photos = self.p.get_records_count()

        txt = (f'<b>Статистика</b>\n'
        + f'• Кабаны: <b>{boars}</b>\n'
        + f'• Премиум кабаны: <b>{premium_boars}</b>\n'
        + f'• Пользователи: <b>{users}</b>\n'
        + f'• ВК Пользователи: <b>{vk_users}</b>\n'
        + f'• Анекдоты: <b>{jokes}</b>\n'
        + f'• Картинки: <b>{photos}</b>\n')
        return txt
    
    def get_counts(self) -> str:
        cursor = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        cols = list(map(lambda x: x[0], cursor.description))
        counts = []
        for i in range(len(cols)):
            counts.append(self.get_record(row=0, col=i))
        txt = (f'<b>Количественная</b>\n'
        + f'• Кол-во всех открытых кабанов: <b>{counts[0]}</b>\n'
        + f'• Кол-во нажатий \"какой я кабан сегодня\": <b>{counts[1]}</b>\n'
        + f'• Кол-во нажатий \"анекдот\": <b>{counts[2]}</b>\n'
        + f'• Кол-во нажатий \"фотокарточка\": <b>{counts[3]}</b>\n')
        return txt

    def update_boar(self) -> None:
        new = self.get_record(row=0, col=0) + 1
        self._bd_cursor.execute(f'UPDATE stats SET boars = {new}')
        self._bd.commit()

    def update_wct(self) -> None:
        new = self.get_record(row=0, col=1) + 1
        self._bd_cursor.execute(f'UPDATE stats SET wct_button = {new}')
        self._bd.commit()

    def update_joke(self) -> None:
        new = self.get_record(row=0, col=2) + 1
        self._bd_cursor.execute(f'UPDATE stats SET joke_button = {new}')
        self._bd.commit()

    def update_photo(self) -> None:
        new = self.get_record(row=0, col=3) + 1
        self._bd_cursor.execute(f'UPDATE stats SET photo_button = {new}')
        self._bd.commit()

