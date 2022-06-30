import sqlite3
import config
from utils.logger import log
import threading

lock = threading.Lock()

#      DB structure
# 
#      +---------------------------------+
#      |TABLES         |COLUMNS          |
#      |===============|=================|
#      |accPics________|_________________|
#      |               |fileID:  STRING  |
#      |pics___________|_________________|
#      |               |fileID:  STRING  |
#      |adminJokes_____|_________________|
#      |               |joke:    STRING  |
#      |userJokes______|_________________|
#      |               |joke:    STRING  |
#      |boarsID________|_________________|
#      |               |ID:      STRING  |
#      |msgs___________|_________________|
#      |               |msg:     STRING  |
#      |               |fileID:  STRING  |
#      |users__________|_________________|
#      |               |userID:  INTEGER |
#      |               |wctID:   INTEGER |
#      |               |prevDay: INTEGER |
#      +---------------------------------+


class DB():
    def __init__(self) -> None:
        self.bd = sqlite3.connect(config.db_path, check_same_thread=False)
        self.bd_cursor = self.bd.cursor()
        self.table = ''
        self.col = ''


    def delRecord(self, record) -> None:
        try:
            lock.acquire(True)
            log.info("Удаление записи БД в таблице: " + self.table + " Столбец: " + self.col)
            self.bd_cursor.execute( f'DELETE FROM {self.table} WHERE {self.col}=?', (record, ) )
            self.bd.commit()
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            log.info("Успешно")
            lock.release()


    def newRecord(self, record: str) -> None:
        try:
            lock.acquire(True)
            log.info("Новая запись БД в таблице: " + self.table + " Столбец: " + self.col)
            self.bd_cursor.execute(f'INSERT INTO {self.table} ({self.col}) VALUES (?)', (record, ) ) 
            self.bd.commit()
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            log.info("Успешно")
            lock.release()


    def hasRecords(self) -> bool:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
            record = self.bd_cursor.fetchall()
            if len(record) == 0: return False
            else: return True
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    # in case of often uses recursive cursors, I had to use threading lock
    def getRecCount(self) -> int:
        try:
            lock.acquire(True)
            log.info("Количество записей БД в таблице: " + self.table)
            info = self.bd_cursor.execute(f"SELECT * FROM {self.table}")
            record = self.bd_cursor.fetchall()
            return len(record)
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    def getRecord(self, recNum: int) -> str:
        try:
            lock.acquire(True)    
            info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
            record = self.bd_cursor.fetchall()
            rec = record[recNum]
            return rec[0]
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()

    
    def getTableName(self) -> str:
        return self.table


    def getColName(self) -> str:
        return self.col

    
    def setTableName(self, tableName) -> None:
        setattr(self, "table", tableName)

    
    def setColName(self, colName) -> None:
        setattr(self, "col", colName)


class UserDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "users"
        self.col = 'userID'

    
    def getUsersList(self) -> list:
        try:
            lock.acquire(True)
            log.info("Getting users list")
            info = self.bd_cursor.execute(f'SELECT userID FROM {self.table}')
            records = self.bd_cursor.fetchall()
            records_listed = [record[0] for record in records]
            log.info("Успешно")
            # records_listed is integer list
            return records_listed
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    def getWctForUser(self, userID: int) -> str:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT wctID FROM {self.table} WHERE userID={userID}')
            return self.bd_cursor.fetchall()[0][0] # list > tuple > string
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    def setWctForUser(self, userID: int, boarID: str) -> None:
        try:
            lock.acquire(True)
            log.info("Установка wct для пользователя")
            self.bd_cursor.execute(f'UPDATE {self.table} SET wctID = {boarID} WHERE userID={userID}')
            self.bd.commit()
            log.info("Успешно")
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()

    
    def getPrevDay(self, userID: int) -> int:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT prevDay FROM {self.table} WHERE userID={userID}')
            return self.bd_cursor.fetchall()[0][0] # list > tuple > string
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()

    
    def setPrevDay(self, day: int, userID: int) -> None:
        try:
            lock.acquire(True)
            log.info("Установка предыдущего дня")
            self.bd_cursor.execute(f'UPDATE {self.table} SET prevDay = {day} WHERE userID={userID}')
            self.bd.commit()
            log.info("Успешно")
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    def addUser(self, userID: str) -> None:
        try:
            lock.acquire(True)
            log.info("Auth -- Добавление пользователя в БД")
            self.bd_cursor.execute(f'INSERT INTO {self.table} (userID) VALUES (?)', (userID, ) )
            self.bd.commit()
            log.info("Успешно")
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


class JokeDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self.table = table
        self.col = 'joke'


class MsgDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "msgs"
        self.col = 'msg'


    def getFileID(self, recNum: int) -> str:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT fileID FROM {self.table}')
            record = self.bd_cursor.fetchall()
            msg = record[recNum]
            return msg[0]
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    # new record with file id of photo sent to admin
    def newFileID(self, record: str) -> None:
        try:
            lock.acquire(True)
            log.info("Новая запись БД в таблице: " + self.table + " Столбец: fileID")
            self.bd_cursor.execute(f'INSERT INTO {self.table} (fileID) VALUES (?)', (record, ) ) 
            self.bd.commit()
            log.info("Успешно")
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


    # new record with caption below photo sent to admin
    def insertMsgForFileID(self, msg: str, fileID: str) -> None:
        try:
            lock.acquire(True)
            log.info("Вставка сообщения для картинки")
            self.bd_cursor.execute(f'UPDATE {self.table} SET msg = {msg} WHERE fileID={fileID}')
            self.bd.commit()
            log.info("Успешно")
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self.table = table
        self.col = 'fileID'
    
    
    def getPicID(self, recNum: int) -> str:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
            record = self.bd_cursor.fetchall()
            picID = record[recNum]
            return picID[0]
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


class BoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "boarsID"
        self.col = "ID"


    def getID(self, recNum: int) -> str:
        try:
            lock.acquire(True)
            info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
            record = self.bd_cursor.fetchall()
            ID = record[recNum]
            return ID[0]
        except Exception as e:
            log.error(e)
            print(e)
        finally:
            lock.release()


class Statistics(DB):
    def __init__(self) -> None:
        super().__init__()
        self.b = BoarDB()
        self.u = UserDB()
        self.j = JokeDB("adminJokes")
        self.p = PicDB("accPics")


    def get(self) -> str:
        txt = f"<b>Статистика</b>\n•Кабаны: <b>{self.b.getRecCount()}</b>\n•Пользователи: <b>{self.u.getRecCount()}</b>\n•Анекдоты: <b>{self.j.getRecCount()}</b>\n•Картинки: <b>{self.p.getRecCount()}</b>"
        return txt


class new_suggestions(DB):
    def __init__(self) -> None:
        super().__init__()
        self.tables = ['pics', 'userJokes', 'msgs']
    

    def exist(self) -> bool:
        exist = False
        self.photo = 0
        self.jokes = 0
        self.msgs = 0

        for table in self.tables:
            self.table = table
            count = self.getRecCount()
            if count > 0:
                exist = True
                if self.table == "pics":
                    self.photo = count
                elif self.table == "userJokes":
                    self.jokes = count
                elif self.table == "msgs":
                    self.msgs = count
        return exist


    def getMsg(self) -> str:
        msg = f"Админ меню.\nКартинок: {self.photo}. Сообщений: {self.msgs}. Анекдотов: {self.jokes}"
        return msg
