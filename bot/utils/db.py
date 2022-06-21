import sqlite3
from utils.logger import log


class DB():
    def __init__(self) -> None:
        self.bd = sqlite3.connect('../db/main.db', check_same_thread=False)
        self.bd_cursor = self.bd.cursor()
        self.table = ''
        self.col = ''


    def delRecord(self, table, col, record) -> None:
        log.info("Удаление записи БД в таблице: " + table + " Столбец: " + col)
        self.bd_cursor.execute( f'DELETE FROM {table} WHERE {col}=?', (record, ) )
        self.bd.commit()
        log.info("Успешно")


    def newRecord(self, table, col, record) -> None:
        log.info("Новая запись БД в таблице: " + table + " Столбец: " + col)
        self.bd_cursor.execute(f'INSERT INTO {table} ({col}) VALUES (?)', (record, ) ) 
        self.bd.commit()
        log.info("Успешно")


    def getRecCount(self, table) -> int:
        log.info("Количество записей БД в таблице: " + table)
        info = self.bd_cursor.execute(f"SELECT * FROM {table}")
        record = self.bd_cursor.fetchall()
        return len(record)


    def getSelfRecCount(self) -> int:
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
        self.col = 'id'

    
    def getUsersList(self) -> list:
        info = self.bd_cursor.execute('SELECT userID FROM users')
        records = self.bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        return records_listed


    def getWctForUser(self, userID: int) -> str:
        info = self.bd_cursor.execute(f'SELECT wctID FROM users WHERE userID={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string


    def setWctForUser(self, userID: int, boarID: str) -> None:
        log.info("Установка wct для пользователя")
        self.bd_cursor.execute(f'UPDATE users SET wctID = {boarID} WHERE userID={userID}')
        self.bd.commit()
        log.info("Успешно")

    
    def getPrevDay(self, userID: int) -> int:
        info = self.bd_cursor.execute(f'SELECT prevDay FROM users WHERE userID={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string

    
    def setPrevDay(self, day: int, userID: int) -> None:
        log.info("Установка предыдущего дня")
        self.bd_cursor.execute(f'UPDATE users SET prevDay = {day} WHERE userID={userID}')
        self.bd.commit()
        log.info("Успешно")


    def addUser(self, userID: str) -> None:
        log.info("Auth -- Добавление пользователя в БД")
        self.bd_cursor.execute('INSERT INTO users (userID) VALUES (?)', (userID, ) )
        self.bd.commit()
        log.info("Успешно")


class JokeDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "adminJokes"
        self.col = 'joke'


    def getJoke(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM adminJokes')
        record = self.bd_cursor.fetchall()
        joke = record[recNum]
        return joke[0]


    def seeJoke(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM userJokes')
        record = self.bd_cursor.fetchall()
        joke = record[recNum]
        return joke[0]


    def hasJokes(self) -> bool:
        info = self.bd_cursor.execute('SELECT * FROM userJokes')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False
        else: return True


class MsgDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "msgs"
        self.col = 'msg'


    def getMsg(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM msgs')
        record = self.bd_cursor.fetchall()
        msg = record[recNum]
        return msg[0]


    def hasMsg(self) -> bool:
        info = self.bd_cursor.execute('SELECT * FROM msgs')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False
        else: return True


    def seeMsg(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM msgs')
        record = self.bd_cursor.fetchall()
        msg = record[recNum]
        return msg[0]


class PicDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "pics"
        self.col = 'fileID'
    

    def hasPics(self) -> bool:
        info = self.bd_cursor.execute('SELECT * FROM pics')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False

    
    def getPicID(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM accPics')
        record = self.bd_cursor.fetchall()
        picID = record[recNum]
        return picID[0]


class BoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "boarsID"
        self.col = "ID"


    def getID(self, recNum: int) -> str:
        info = self.bd_cursor.execute('SELECT * FROM boarsID')
        record = self.bd_cursor.fetchall()
        ID = record[recNum]
        return ID[0]


#кабаны юзеры шутки фотки
class Statistics(DB):
    def __init__(self) -> None:
        super().__init__()
        self.b = BoarDB()
        self.u = UserDB()
        self.j = JokeDB()
        self.p = PicDB()


    def get(self) -> str:
        txt = f"<b>Статистика</b>\n•Кабаны: {self.b.getSelfRecCount()}\n•Пользователи: {self.u.getSelfRecCount()}\n•Анекдоты: {self.j.getSelfRecCount()}\n•Картинки: {self.p.getSelfRecCount()}"
        return txt