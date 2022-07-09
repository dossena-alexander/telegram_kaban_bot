import sqlite3
from config import PATH, UPLOAD_LIMIT
from utils.logger import log
import threading

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
#      |               |userID: |wctID: |prevDay: |premium: |uploadCount:|
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
        self.bd = sqlite3.connect(PATH.DB, check_same_thread=False)
        self.bd_cursor = self.bd.cursor()
        self.table = ''
        self.col = ''


    @lock_thread
    def delRecord(self, record) -> None:
        log.info("Удаление записи БД в таблице: " + self.table + " Столбец: " + self.col)
        self.bd_cursor.execute( f'DELETE FROM {self.table} WHERE {self.col}=?', (record, ) )
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def newRecord(self, record: str) -> None:
        log.info("Новая запись БД в таблице: " + self.table + " Столбец: " + self.col)
        self.bd_cursor.execute(f'INSERT INTO {self.table} ({self.col}) VALUES (?)', (record, ) ) 
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def hasRecords(self) -> bool:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        if len(record) == 0: return False
        else: return True


    @lock_thread
    def getRecCount(self) -> int:
        log.info("Количество записей БД в таблице: " + self.table)
        info = self.bd_cursor.execute(f"SELECT * FROM {self.table}")
        record = self.bd_cursor.fetchall()
        log.error(len(record))
        return len(record)


    @lock_thread
    def getRecord(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        rec = record[recNum]
        return rec[0]

    
    def getTableName(self) -> str:
        return self.table


    def getColName(self) -> str:
        return self.col

    
    def setTableName(self, tableName) -> None:
        setattr(self, "table", tableName)

    
    def setColName(self, colName) -> None:
        setattr(self, "col", colName)




class UserDB(DB):
    def __init__(self, table = "users", col = "userID") -> None:
        super().__init__()
        self.table = table
        self.col = col


    @lock_thread
    def getUsersList(self) -> list:
        log.info("Getting users list")
        info = self.bd_cursor.execute(f'SELECT {self.col} FROM {self.table}')
        records = self.bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        log.info("Успешно")
        # records_listed is integer list
        return records_listed


    @lock_thread
    def getWctForUser(self, userID: int) -> str:
        info = self.bd_cursor.execute(f'SELECT wctID FROM {self.table} WHERE {self.col}={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string


    @lock_thread
    def setWctForUser(self, userID: int, boarID: str) -> None:
        log.info("Установка wct для пользователя")
        self.bd_cursor.execute(f'UPDATE {self.table} SET wctID = {boarID} WHERE {self.col}={userID}')
        self.bd.commit()
        log.info("Успешно")


    @lock_thread    
    def getPrevDay(self, userID: int) -> int:
        info = self.bd_cursor.execute(f'SELECT prevDay FROM {self.table} WHERE {self.col}={userID}')
        return self.bd_cursor.fetchall()[0][0] # list > tuple > string

    
    @lock_thread
    def setPrevDay(self, day: int, userID: int) -> None:
        log.info("Установка предыдущего дня")
        self.bd_cursor.execute(f'UPDATE {self.table} SET prevDay = {day} WHERE {self.col}={userID}')
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def addUser(self, userID: str) -> None:
        log.info("Auth -- Добавление пользователя в БД")
        self.bd_cursor.execute(f'INSERT INTO {self.table} ({self.col}) VALUES (?)', (userID, ) )
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def checkPremium(self, userID) -> bool:
        info = self.bd_cursor.execute(f'SELECT premium FROM {self.table} WHERE {self.col}={userID}')
        premium = self.bd_cursor.fetchall()[0][0] # list > tuple > string
        if premium == 0:
            return False
        else:
            return True


    @lock_thread
    def setPremium(self, userID) -> None:
        log.info("Установка premium")
        self.bd_cursor.execute(f'UPDATE {self.table} SET premium = 1 WHERE {self.col}={userID}')
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def loosePremium(self, userID) -> None:
        log.info("Потеря premium")
        self.bd_cursor.execute(f'UPDATE {self.table} SET premium = 0 WHERE {self.col}={userID}')
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def newUpload(self, userID) -> None:
            log.info("Новая загрузка")
            count = self.getUploadCount(userID) + 1
            self.bd_cursor.execute(f'UPDATE {self.table} SET uploadCount = {count} WHERE {self.col}={userID}')
            self.bd.commit()
            log.info("Успешно")


    def getUploadCount(self, userID) -> int:
        try:
            log.error("МОДУЛЬ БЕЗ БЛОКИРОВКИ ПОТОКА")
            info = self.bd_cursor.execute(f'SELECT uploadCount FROM {self.table} WHERE {self.col}={userID}')
            count = self.bd_cursor.fetchall()[0][0] # list > tuple > string
            log.error("УСПЕШНО")
            return count
        except Exception as e:
            log.error(e)
            print(e)


    @lock_thread
    def uploadsLimitReached(self, userID) -> bool:
        info = self.bd_cursor.execute(f'SELECT uploadCount FROM {self.table} WHERE {self.col}={userID}')
        count = self.bd_cursor.fetchall()[0][0] # list > tuple > string
        if count >= UPLOAD_LIMIT.COUNT:
            return True
        else:
            return False


    @lock_thread
    def uploadsDel(self, userID) -> None:
        log.info("Списывание счетчика загрузок")
        count = self.getUploadCount(userID)
        self.bd_cursor.execute(f'UPDATE {self.table} SET uploadCount = 0 WHERE {self.col}={userID}')
        self.bd.commit()
        log.info("Успешно")




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


    @lock_thread
    def getFileID(self, recNum: int) -> str:
        info = self.bd_cursor.execute(f'SELECT fileID FROM {self.table}')
        record = self.bd_cursor.fetchall()
        msg = record[recNum]
        return msg[0]


    @lock_thread
    def delAll(self, recNum: int) -> None:
        log.info("Удаление записи БД в таблице: " + self.table + " Столбец: fileID")
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        rec = self.bd_cursor.fetchall()[recNum]
        msg = rec[0]
        fileID = rec[1]
        self.bd_cursor.execute( f'DELETE FROM {self.table} WHERE msg=? OR fileID=?', (msg, fileID) )
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    def msgHasFileID(self, recNum: int) -> bool:
        info = self.bd_cursor.execute(f'SELECT * FROM {self.table}')
        record = self.bd_cursor.fetchall()
        if record[recNum][1] == None:
            return False
        else:
            return True


    # new record with file id of photo sent to admin
    @lock_thread
    def newFileID(self, record: str) -> None:
        log.info("Новая запись БД в таблице: " + self.table + " Столбец: fileID")
        self.bd_cursor.execute(f'INSERT INTO {self.table} (fileID) VALUES (?)', (record, ) ) 
        self.bd.commit()
        log.info("Успешно")


    @lock_thread
    # new record with caption below photo sent to admin
    def insertMsgForFileID(self, msg: str, fileID: str) -> None:
        log.info("Вставка сообщения для картинки")
        self.bd_cursor.execute(f'UPDATE {self.table} SET msg=\'{msg}\' WHERE fileID=\'{fileID}\'')
        self.bd.commit()
        log.info("Успешно")




class PicDB(DB):
    def __init__(self, table) -> None:
        super().__init__()
        self.table = table
        self.col = 'fileID'
    



class BoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "boarsID"
        self.col = "ID"




class PremiumBoarDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table = "premiumBoarsID"
        self.col = "ID"


    @lock_thread
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
        self.vk_u = UserDB("vk_users", "vk_id")
        self.j = JokeDB("adminJokes")
        self.p = PicDB("accPics")


    def get(self) -> str:
        txt = f"<b>Статистика</b>\n•Кабаны: <b>{self.b.getRecCount()}</b>\n•Пользователи: <b>{self.u.getRecCount()}</b>\n•ВК Пользователи: <b>{self.vk_u.getRecCount()}</b>\n•Анекдоты: <b>{self.j.getRecCount()}</b>\n•Картинки: <b>{self.p.getRecCount()}</b>"
        return txt




class suggestions(DB):
    # when users upload photo or joke counter increases to the limit, then bot sends message to admin
    limit = UPLOAD_LIMIT.COUNT 
    counter = 0


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


    def reachedLimit(self) -> bool:
        if self.counter >= self.limit:
            self.counter = 0
            return True
        else:
            return False

    
    def new_suggest(self) -> None:
        self.counter += 1


    def getMsg(self) -> str:
        msg = f"Админ меню.\nКартинок: {self.photo}. Сообщений: {self.msgs}. Анекдотов: {self.jokes}"
        return msg
