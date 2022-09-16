import os
import sqlite3
from datetime import date, datetime, timedelta, timezone, time
from config import PATH, STAT_COLLECTOR_LOCK
from server.utils.db import lock_thread


class Time():
    time: str
    hour: int
    minute: int
    second: int
    _msc_offset = 3
    msc_tz = timezone(timedelta(hours=_msc_offset), name='msc')


    def __init__(self, hour = None, 
                       minute = None, 
                       second = None, 
                       now = False) -> None:
        if now == True:
            date = datetime.now(self.msc_tz)
            hour = date.hour
            minute = date.minute
            second = date.second
            del date
        else:
            if hour == None:
                hour = 0
            if minute == None:
                minute = 0
            if second == None:
                second = 0
        self.hour = hour
        self.minute = minute
        self.second = second
        self.time = time(hour, minute, second, tzinfo=self.msc_tz).strftime('%H:%M:%S')

    @classmethod
    def now(cls):
        return datetime.now(cls.msc_tz).strftime('%H:%M:%S')

    def __repr__(self) -> str:
        return str(self.time)


class TimeInterval():
    time: tuple[Time, Time]


    def __init__(self, start: Time, end: Time) -> None:
        self.time = (start, end)

    def __repr__(self) -> tuple[Time, Time]:
        return self.time

    def __getitem__(self, item: int) -> Time:
        return self.time[item]


class ClickCollectorObserver():
    time: Time


    def __init__(self) -> None:
        time = Time(now=True)
        self.time = time.time
        self.hour = time.hour

    def new_hour(self) -> bool:
        if self.same_hour():
            return False
        return True

    def new_time(self) -> None:
        self.time = Time.now()

    def get_time(self) -> str:
        return self.time

    def same_hour(self) -> bool:
        now_hour = Time(now=True).hour
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
        year = str(date.today().year) + '/'
        month = str(date.today().month) + '/'
        self._make_dir(PATH.DB_STATS+year+month)
        self.db = sqlite3.connect(PATH.DB_STATS+year+month+db_name, check_same_thread=False)
        self.db_cursor = self.db.cursor()

    def create_table(self, target: str):
        """If new DB has no tables"""
        self.db_cursor.execute(f'CREATE TABLE {target} (time TIME, clicks INTEGER DEFAULT (0) )')
        self.db.commit()

    def new_row(self, target, time):
        self.db_cursor.execute(f'INSERT INTO {target} (time, clicks) VALUES (?, ?)', (time, 0) )  
        self.db.commit()

    def set_date(self, date: date) -> None:
        self.date = date

    @lock_thread
    def insert(self, target: str, time: str, clicks: int) -> None:
        db_name = self._current_date_db_name()   
        self.connect(db_name)
        try:
            self.db_cursor.execute(f'INSERT INTO {target} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        except:
            self.create_table(target)
            self.db_cursor.execute(f'INSERT INTO {target} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        self.db.commit()

    @lock_thread
    def update_clicks(self, target: str, time: str) -> None:
        db_name = self._current_date_db_name()
        self.connect(db_name)
        clicks = 0
        try:
            self.db_cursor.execute(f'SELECT clicks FROM {target} WHERE time = \'{time}\'')
            clicks = self.db_cursor.fetchall()[0][0] 
        except:
            try:
                self.create_table(target)
            except:
                self.new_row(target, time)
            self.db_cursor.execute(f'SELECT clicks FROM {target} WHERE time = \'{time}\'')
            clicks = self.db_cursor.fetchall()[0][0] 
        self.db_cursor.execute(f'UPDATE {target} SET clicks = {clicks + 1} WHERE time = \'{time}\'') 
        self.db.commit()

    @lock_thread
    def get(self, from_target: str, # Table name
                  time_interval: TimeInterval) -> tuple[list[str], list[int]]:
        start_time = time_interval[0].time
        end_time = time_interval[1].time
        self.db_cursor.execute(f'SELECT time FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
        times = self.db_cursor.fetchall()
        times = [time[0] for time in times]
        self.db_cursor.execute(f'SELECT clicks FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
        clicks = self.db_cursor.fetchall()
        clicks = [click[0] for click in clicks]
        return times, clicks

    def _make_dir(self, path: str):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    def _now_day(self, full_date = False):
        now = date.today() # yyyy-mm-dd
        if full_date:
            return str(now)
        return now.day

    def _current_date_db_name(self):
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
                       target_time_interval = TimeInterval(Time(0, 0, 0), Time(23, 59, 59))) -> None:
        """
        Args:
            from_target (str): Table name\n
            target_date (date): In format: YYYY-MM-DD\n
            target_time_interval (TimeInterval) = ('00:00:00', '23:59:59') | Any\n
        """
        self.from_target = from_target
        self.target_date = target_date
        self.target_time_interval = target_time_interval
        self._prep_data()

    def get_data(self) -> tuple[list[datetime], list[int]]:
        """
        Returns:
            Hours interval (list) and clicks (list) for a day
        """
        return self.times, self.clicks

    def _prep_data(self):
        db = ClickCollectorDB(self.target_date)
        self.times, self.clicks = db.get(self.from_target, 
                                    self.target_time_interval[0].time, 
                                    self.target_time_interval[1].time)
        del db

    def get_clicks_sum(self) -> int:
        clicks = sum(self.clicks)
        return clicks

    def get_times(self) -> list[str]:
        return self.times


class DateStatClickCollector(IStatClickCollector):
    """Use this if you need statistics for days, not for a day"""
    default_time_interval = TimeInterval(Time(0, 0, 0), Time(23, 59, 59))
    time_interval: TimeInterval


    def __init__(self, from_target: str,
                       date_interval: tuple[datetime, datetime],
                       time_interval = default_time_interval) -> None:
        self.from_target = from_target
        self.time_interval = time_interval
        self.date_interval = date_interval

    def get_data(self, time_interval = None) -> tuple[list[datetime], list[int]]:
        """
        Returns:
            tuple[list[datetime], list[int]]: list of dates (days) and clicks per day
        """
        if not time_interval:
            time_interval = self.time_interval
        dates_interval = self.prep_dates(self.date_interval)
        clicks = []
        for date in dates_interval:
            statClickCollector = DayStatClickCollector(self.from_target, date, time_interval)
            clicks.append(statClickCollector.get_clicks_sum())
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
