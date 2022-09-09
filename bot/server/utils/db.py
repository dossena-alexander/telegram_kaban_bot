import sqlite3
import threading

from config import PATH, PREMIUM_LIMIT
from server.utils.logger import log


lock = threading.Lock() # thread_lock for DB cursor


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
            info = self._bd_cursor.execute(f'SELECT uploadCount FROM {self._table} WHERE {self._column}={userID}')
            uploads_count = self._bd_cursor.fetchall()[0][0] # list > tuple > string
            return uploads_count
        except Exception as e:
            log.error('Method userDB.get_uploads_count' + e)
            print('Method userDB.get_uploads_count' + e)

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
    def get_premium_turned_day(self, userID: int) -> int:
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
        try:
            self._bd_cursor.execute(f'SELECT {boar_category} FROM {self._table} WHERE {self._column}={userID}')
            boars = self._bd_cursor.fetchall()[0][0] # list > tuple > string
            return boars
        except Exception as e:
            print('Method userDB._all_boars' + e)
            log.error('Method userDB._all_boars' + e)

    @lock_thread
    def get_user_boars(self, userID: int, boar_category: str) -> str:
        return self._all_boars(userID, boar_category)

    @lock_thread
    def new_boar_for_user(self, userID: int, boar: str, boar_category: str) -> None:
        new_boar = f"{self._all_boars(userID, boar_category)}, {boar}"
        self._bd_cursor.execute(f'UPDATE {self._table} SET {boar_category} = \'{new_boar}\' WHERE {self._column}={userID}')
        self._bd.commit()

    def _get_upload_count(self, column: str, user_id: int) -> None:
        self._bd_cursor.execute(f'SELECT {column} FROM {self._table} WHERE {self._column}={user_id}')
        upload = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        return upload

    @lock_thread
    def get_upload_count(self, column: str, user_id: int) -> None:
        """Available columns: photo_upload, joke_upload, admin_msg

        Args:
            column (str): One of those cols
            user_id (int): TG user id

        Returns:
            int: Count of uploads
        """
        return self._get_upload_count(column, user_id)

    @lock_thread
    def new_photo_upload(self, user_id: int) -> None:
        new_upload = self._get_upload_count('photo_upload', user_id) + 1
        self._bd_cursor.execute(f'UPDATE {self._table} SET photo_upload = {new_upload} WHERE {self._column}={user_id}')
        self._bd.commit()

    @lock_thread
    def new_joke_upload(self, user_id: int) -> None:
        new_upload = self._get_upload_count('joke_upload', user_id) + 1
        self._bd_cursor.execute(f'UPDATE {self._table} SET joke_upload = {new_upload} WHERE {self._column}={user_id}')
        self._bd.commit()

    @lock_thread
    def new_admin_msg(self, user_id: int) -> None:
        new_upload = self._get_upload_count('admin_msg', user_id) + 1
        self._bd_cursor.execute(f'UPDATE {self._table} SET admin_msg = {new_upload} WHERE {self._column}={user_id}')
        self._bd.commit()

    @lock_thread
    def get_upload_day(self, user_id: int) -> int:
        self._bd_cursor.execute(f'SELECT upload_day FROM {self._table} WHERE {self._column}={user_id}')
        day = self._bd_cursor.fetchall()[0][0] # list > tuple > string
        return day

    @lock_thread
    def update_upload_day(self, user_id: int, day: int) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET upload_day = {day} WHERE {self._column}={user_id}')
        self._bd.commit()

    @lock_thread
    def can_send_notification(self, user_id: int) -> bool:
        self._bd_cursor.execute(f'SELECT notify_option FROM {self._table} WHERE {self._column}={user_id}')
        option = self._bd_cursor.fetchall()[0][0]
        if option == 0:
            return False
        return True

    @lock_thread
    def update_notify_option(self, user_id: int, option: bool) -> None:
        notify = 0
        if option == True:
            notify = 1
        self._bd_cursor.execute(f'UPDATE {self._table} SET notify_option = {notify} WHERE {self._column}={user_id}')
        self._bd.commit()


class JokeDB(DB):
    def __init__(self, table: str) -> None:
        super().__init__()
        self._table = table
        self._column = 'joke'

    @lock_thread
    def insert(self, joke: str, user_id: int, user_name: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}, user_id, user_name) VALUES (?, ?, ?)', (joke, user_id, user_name) ) 
        self._bd.commit()


class MsgDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "msgs"
        self._column = 'msg'

    @lock_thread
    def insert(self, message: str, user_id: int, user_name: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}, user_id, user_name) VALUES (?, ?, ?)', (message, user_id, user_name) ) 
        self._bd.commit()

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
    def new_file_id(self, record: str, user_id: int, user_name: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} (fileID, user_id, user_name) VALUES (?, ?, ?)', (record, user_id, user_name) ) 
        self._bd.commit()

    # new record with caption below photo sent to admin
    @lock_thread
    def update_msg_for_file_id(self, msg: str, fileID: str) -> None:
        self._bd_cursor.execute(f'UPDATE {self._table} SET msg=\'{msg}\' WHERE fileID=\'{fileID}\'')
        self._bd.commit()


class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self._table = table
        self._column = 'fileID'
        self._column_2 = 'tg_id'
        self._column_3 = 'user_id'
        self._column_4 = 'user_name'


    @lock_thread
    def insert(self, file_name: str, file_id: str, user_id: int, user_name: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}, {self._column_2}, {self._column_3}, {self._column_4}) VALUES (?, ?, ?, ?)', (file_name, file_id, user_id, user_name) ) 
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
        """Needs a name of boar from DB. Returns category of boar

        Args:
            boarID (str): For example: file_231.jpg

        Returns:
            str: Category of boar you sent to method
        """
        columns = self._get_columns_names()
        for column in columns:
            boars = self.get_boars_of_category(column)
            if boarID in boars:
                return column

    @lock_thread
    def new_boar(self, boar_category: str, boar: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({boar_category}) VALUES (?)', (boar, ) ) 
        self._bd.commit()

