import sqlite3
from utils.logger import log

pathToDB = '../db/main.db'

# DB structure
#      +---------------------------------+
#      |TABLES         |columns          |
#      |===============|=================|
#      |accPics________|_________________|
#      |               |fileID: STRING   |
#      |pics___________|_________________|
#      |               |fileID: STRING   |
#      |adminJokes_____|_________________|
#      |               |joke: STRING     |
#      |userJokes______|_________________|
#      |               |joke: STRING     |
#      |boarsID________|_________________|
#      |               |ID: STRING       |
#      |msgs___________|_________________|
#      |               |msg: STRING      |
#      |users__________|_________________|
#      |               |userID: INTEGER  |
#      |               |wctID: STRING    |
#      |               |prevDay: INTEGER |
#      +---------------------------------+


class DB():
    def __init__(self) -> None:
        self.bd = sqlite3.connect(pathToDB, check_same_thread=False)
        self.bd_cursor = self.bd.cursor()
        self.table = ''
        self.col = ''


    def delRecord(self, record) -> None:
        log.info("Удаление записи БД в таблице: " + self.table + " Столбец: " + self.col)
        self.bd_cursor.execute( f'DELETE FROM {self.table} WHERE {self.col}=?', (record, ) )
        self.bd.commit()
        log.info("Успешно")


    def newRecord(self, record) -> None:
        log.info("Новая запись БД в таблице: " + self.table + " Столбец: " + self.col)
        self.bd_cursor.execute(f'INSERT INTO {self.table} ({self.col}) VALUES (?)', (record, ) ) 
        self.bd.commit()
        log.info("Успешно")


    def getRecCount(self) -> int:
        log.info("Количество записей БД в таблице: " + self.table)
        info = self.bd_cursor.execute(f"SELECT * FROM {self.table}")
        record = self.bd_cursor.fetchall()
        return len(record)

    
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
        info = self.bd_cursor.execute(f'SELECT userID FROM {self.table}')
        records = self.bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        return records_listed


    def getWctForUser(self, userID: int) -> str:
        info = self.bd_cursor.execute(f'SELECT wctID FROM {self.table} WHERE userID={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string


    def setWctForUser(self, userID: int, boarID: str) -> None:
        log.info("Установка wct для пользователя")
        self.bd_cursor.execute(f'UPDATE {self.table} SET wctID = {boarID} WHERE userID={userID}')
        self.bd.commit()
        log.info("Успешно")

    
    def getPrevDay(self, userID: int) -> int:
        info = self.bd_cursor.execute(f'SELECT prevDay FROM {self.table} WHERE userID={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string

    
    def setPrevDay(self, day: int, userID: int) -> None:
        log.info("Установка предыдущего дня")
        self.bd_cursor.execute(f'UPDATE {self.table} SET prevDay = {day} WHERE userID={userID}')
        self.bd.commit()
        log.info("Успешно")


    def addUser(self, userID: str) -> None:
        log.info("Auth -- Добавление пользователя в БД")
        self.bd_cursor.execute('INSERT INTO {self.table} (userID) VALUES (?)', (userID, ) )
        self.bd.commit()
        log.info("Успешно")


class JokeDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self.table = table
        self.col = 'joke'


    def getJoke(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        joke = record[recNum]
        return joke[0]


    def hasJokes(self) -> bool:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False
        else: return True


class MsgDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "msgs"
        self.col = 'msg'


    def getMsg(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        msg = record[recNum]
        return msg[0]


    def hasMsg(self) -> bool:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False
        else: return True


    def seeMsg(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        msg = record[recNum]
        return msg[0]


class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self.table = table
        self.col = 'fileID'
    

    def hasPics(self) -> bool:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False

    
    def getPicID(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        picID = record[recNum]
        return picID[0]


class BoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "boarsID"
        self.col = "ID"


    def getID(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        ID = record[recNum]
        return ID[0]


class Statistics(DB):
    def __init__(self) -> None:
        super().__init__()
        self.b = BoarDB()
        self.u = UserDB()
        self.j = JokeDB()
        self.p = PicDB("accPics")


    def get(self) -> str:
        txt = f"<b>Статистика</b>\n•Кабаны: <b>{self.b.getRecCount()}</b>\n•Пользователи: <b>{self.u.getRecCount()}</b>\n•Анекдоты: <b>{self.j.getRecCount()}</b>\n•Картинки: <b>{self.p.getRecCount()}</b>"
        return txt