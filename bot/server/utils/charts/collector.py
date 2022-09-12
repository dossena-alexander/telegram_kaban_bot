import subprocess
import sqlite3
from datetime import date, datetime, timedelta
from config import PATH, STAT_COLLECTOR_LOCK
from server.utils.db import lock_thread


TIME_ZONE = -3 


class Time():
    """str in format %H:%M:%S
    """
    time: str


    def __init__(self, time: str) -> None:
        self.time = time
        
    def __repr__(self) -> str:
        return self.time

    def convert_str_time(self) -> datetime:
        return datetime.strptime(self.time, "%H:%M:%S")


class TimeInterval():
    time: tuple[Time, Time]


    def __init__(self, start: Time, end: Time) -> None:
        self.time = (start, end)

    def __repr__(self) -> tuple[str, str]:
        return self.time

    def __getitem__(self, item: int) -> Time:
        return self.time[item]

    def convert_str_time(self) -> tuple[datetime, datetime]:
        t = (self.time[0].convert_str_time(), 
             self.time[1].convert_str_time())
        return t


class ClickCollectorObserver():
    time: Time


    def __init__(self) -> None:
        date = datetime.now()
        self.hour = date.hour
        self.time = Time(date.time().strftime('%H:%M:%S'))

    def new_hour(self) -> bool:
        if self.same_hour():
            return False
        return True

    def new_time(self) -> None:
        date = datetime.now()
        self.time = self.time = Time(date.time().strftime('%H:%M:%S'))

    def get_time(self) -> str:
        return self.time

    def same_hour(self) -> bool:
        date = datetime.now()
        now_hour = date.hour
        if now_hour > self.hour:
            self.hour = now_hour
            return False
        return True


class ClickCollectorDB():
    def __init__(self, date = None):
        if date:
            self.date = date
        db_name = self.get_db_name()
        self.connect(db_name)

    def connect(self, db_name: str) -> None:
        # try:
        self.db = sqlite3.connect(PATH.DB_STATS+db_name, check_same_thread=False)
        self.db_cursor = self.db.cursor()
        # except:
        #     subprocess.call(['mv', 'test.db', f'{db_name}'])
        #     self.db = sqlite3.connect(PATH.DB_STATS+db_name, check_same_thread=False)
        #     self.db_cursor = self.db.cursor()

    def create(self, time):
        """If new DB has no tables"""
        self.db_cursor.execute('CREATE TABLE wct_clicks (time TIME, clicks INTEGER DEFAULT (0) )')
        self.db_cursor.execute('INSERT INTO wct_clicks (time, clicks) VALUES (?, ?)', (time, 0) )  
        self.db_cursor.execute('CREATE TABLE photo_clicks (time TIME, clicks INTEGER DEFAULT (0) )') 
        self.db_cursor.execute('INSERT INTO photo_clicks (time, clicks) VALUES (?, ?)', (time, 0) )  
        self.db_cursor.execute('CREATE TABLE joke_clicks (time TIME, clicks INTEGER DEFAULT (0) )') 
        self.db_cursor.execute('INSERT INTO joke_clicks (time, clicks) VALUES (?, ?)', (time, 0) )  
        self.db.commit()

    def set_date(self, date: date) -> None:
        self.date = date

    @lock_thread
    def insert(self, name: str, time: Time, clicks: int) -> None:
        db_name = self._current_day_db_name()   
        self.connect(db_name)
        time = str(time)
        try:
            self.db_cursor.execute(f'INSERT INTO {name} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        except Exception as e:
            self.create(time)
            self.db_cursor.execute(f'INSERT INTO {name} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        self.db.commit()

    @lock_thread
    def update_clicks(self, target: str, time: Time) -> None:
        db_name = self._current_day_db_name()
        self.connect(db_name)
        time = str(time)
        clicks = 0
        try:
            self.db_cursor.execute(f'SELECT clicks FROM {target} WHERE time = \'{time}\'')
            clicks = self.db_cursor.fetchall()[0][0] 
        except:
            self.create(time)
            self.db_cursor.execute(f'SELECT clicks FROM {target} WHERE time = \'{time}\'')
            clicks = self.db_cursor.fetchall()[0][0] 
        self.db_cursor.execute(f'UPDATE {target} SET clicks = {clicks + 1} WHERE time = \'{time}\'') 
        self.db.commit()

    @lock_thread
    def get(self, from_target: str, # Table name
                  start_time: Time, 
                  end_time: Time) -> tuple[list[str], list[int]]:
        start_time = str(start_time)
        end_time = str(end_time)
        self.db_cursor.execute(f'SELECT time FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
        times = self.db_cursor.fetchall()
        times = [time[0] for time in times]
        self.db_cursor.execute(f'SELECT clicks FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
        clicks = self.db_cursor.fetchall()
        clicks = [click[0] for click in clicks]
        return times, clicks

    def _now_day(self, full_date = False):
        now = date.today() # yyyy-mm-dd
        if full_date:
            return str(now)
        return now.day

    def _current_day_db_name(self):
        name = self._now_day(full_date=True)
        return f'{name}.db'

    def get_db_name(self) -> str:
        try:
            name = self.date
        except:
            name = self._now_day(full_date=True)
        return f'{name}.db'


class ClickCollector():
    target: str
    clicks: int


    def __init__(self, target: str) -> None:
        """target could be:
            'wct_clicks'\n
            'photo_clicks'\n
            'joke_clicks'\n
        """
        if not STAT_COLLECTOR_LOCK:
            self.target = target
            self.observer = ClickCollectorObserver()
            self.db = ClickCollectorDB()
            self.clicks = 0

    def new(self) -> None:
        if not STAT_COLLECTOR_LOCK:
            if self.observer.new_hour():
                time = self.observer.get_time()
                self.db.insert(self.target, time, self.clicks)
                self.observer.new_time()
                self.clicks = 0
            self.clicks += 1

    def new_by_db(self) -> None:
        if not STAT_COLLECTOR_LOCK:
            if self.observer.new_hour():
                self.observer.new_time()
            self.db.update_clicks(self.target, self.observer.get_time())


class IStatClickCollector():
    def get_data(self) -> tuple[list[datetime], list[int]]:
        pass


class DayStatClickCollector(IStatClickCollector):
    """Day clicks statistics"""
    target_date: date
    target_time_interval: TimeInterval


    def __init__(self, from_target: str, # Table name
                       target_date: date, # In format: YYYY-MM-DD
                       target_time_interval = TimeInterval('00:00:00', '23:59:59')) -> None:
        """
        Args:
            from_target (str): Table name\n
            target_date (date): In format: YYYY-MM-DD\n
            target_time_interval (TimeInterval) = ('00:00:00', '23:59:59') | Any\n
        """
        self.from_target = from_target
        self.target_date = target_date
        self.target_time_interval = target_time_interval

    def get_data(self) -> tuple[list[datetime], list[int]]:
        """
        Returns:
            Hours interval (list) and clicks (list) for a day
        """
        db = ClickCollectorDB(self.target_date)
        times, self.clicks = db.get(self.from_target, 
                                    self.target_time_interval[0], 
                                    self.target_time_interval[1])
        del db
        return times, self.clicks

    def get_clicks(self) -> int:
        db = ClickCollectorDB(self.target_date)
        _, self.clicks = db.get(self.from_target, 
                                self.target_time_interval[0], 
                                self.target_time_interval[1])
        del db
        clicks = sum(self.clicks)
        return clicks


class DateStatClickCollector(IStatClickCollector):
    """Use this if you need statistics for days, not for a day"""
    default_time_interval = TimeInterval('00:00:00', '23:59:59')


    def __init__(self, from_target: str,
                       date_interval: tuple[datetime, datetime],
                       time_interval = default_time_interval) -> None:
        self.from_target = from_target
        self.default_time_interval = time_interval
        self.date_interval = date_interval

    def get_data(self) -> tuple[list[datetime], list[int]]:
        """
        Returns:
            tuple[list[datetime], list[int]]: list of dates (days) and clicks per day
        """
        dates_interval = self.prep_dates(self.date_interval)
        clicks = []
        for date in dates_interval:
            statClickCollector = DayStatClickCollector(self.from_target, date, self.default_time_interval)
            clicks.append(statClickCollector.get_clicks())
        return dates_interval, clicks

    def prep_dates(self, date_interval: tuple[datetime, datetime]) -> list[datetime]:
        """
        Args:
            date_interval (tuple[datetime, datetime]): Start date and End date of interval

        Returns:
            All dates between start - end dates
        """
        start = datetime.strptime(date_interval[0], '%Y/%M/%D')
        end = datetime.strptime(date_interval[1], '%Y/%M/%D')   

        return [(start + timedelta(days=x)).strftime('%Y/%M/%D') for x in range(0, (end-start).days)]
