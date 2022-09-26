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
            for v in [hour, minute, second]:
                if v == None: v = 0
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

    @property
    def start(self):
        return self.time[0]

    @property
    def end(self):
        return self.time[1]


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
    def __init__(self, date = None, db_name = None):
        if date:
            self.date = date
        if db_name:
            db_name = db_name
        else:
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
        self._insert(target, time, clicks)

    def _insert(self, target, time, clicks):
        db_name = self._current_date_db_name()   
        self.connect(db_name)
        if self.table_exist(target):
            self.db_cursor.execute(f'INSERT INTO {target} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        else:
            self.create_table(target)
            self.db_cursor.execute(f'INSERT INTO {target} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        self.db.commit()

    @lock_thread
    def update_clicks(self, target: str, time: str) -> None:
        db_name = self._current_date_db_name()
        self.connect(db_name)
        clicks = 0
        if self.table_exist(target):
            try:
                self.db_cursor.execute(f'UPDATE {target} SET clicks = {clicks + 1} WHERE time = \'{time}\'') 
            except:
                self._insert(target, time, 1)
        self.db.commit()

    def table_exist(self, target: str) -> bool:
        self.db_cursor.execute(f'SELECT name FROM sqlite_master WHERE type=table AND name={target}')
        if self.db_cursor.fetchall() == 0:
            return False
        return True

    @lock_thread
    def get(self, from_target: str, # Table name
                  time_interval: TimeInterval) -> tuple[list[str], list[int]]:
        start_time = time_interval.start.time
        end_time = time_interval.end.time
        try:
            self.db_cursor.execute(f'SELECT time FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
            times_interval = self.db_cursor.fetchall()
            times = [time[0] for time in times_interval]
        except: # If no such table or column
            times = []
        try:
            self.db_cursor.execute(f'SELECT clicks FROM {from_target} WHERE time BETWEEN \'{start_time}\' AND \'{end_time}\' ') 
            clicks_interval = self.db_cursor.fetchall()
            clicks = [click[0] for click in clicks_interval]
        except: # If no such table or column
            clicks = []

        return times, clicks


    def _make_dir(self, path: str):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    def _now_day(self, full_date = False):
        now = datetime.now(Time.msc_tz).date() # yyyy-mm-dd
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
    _target: str
    _clicks: int


    def __init__(self, target: str) -> None:
        """target could be:
            'wct_clicks'\n
            'photo_clicks'\n
            'joke_clicks'\n
        """
        if not STAT_COLLECTOR_LOCK:
            self._target = target
            self._observer = ClickCollectorObserver()
            self._db = ClickCollectorDB()
            self._clicks = 0

    def new(self) -> None:
        if not STAT_COLLECTOR_LOCK:
            if self._observer.new_hour():
                time = self._observer.get_time()
                self._db.insert(self._target, time, self._clicks)
                self._observer.new_time()
                self._clicks = 0
            self._clicks += 1

    def new_by_db(self) -> None:
        if not STAT_COLLECTOR_LOCK:
            if self._observer.new_hour():
                self._observer.new_time()
            self._db.update_clicks(self._target, self._observer.get_time())


class IStatClickCollector():
    _targets: list[str]
    _target_file: str
    _target_file_date: str
    _data_dict: dict

    
    def __init__(self) -> None:
        self._target_file_date = self._target_file[:-3]

    def get_data(self) -> tuple[list[str], list[int]]:
        return self._data_dict

    def init_dict(self):
        """
        The dict struct is:
        {
            'target': {
                'times': list[str],
                'clicks': list[int]
            }
        }
        """
        return {target: dict.fromkeys(['times', 'clicks']) for target in self._targets}

    @property
    def targets(self) -> list[str]:
        return self._targets

    @property
    def file(self) -> str:
        return self._target_file

    @property
    def date(self) -> str:
        return self._target_file_date


class DayStatClickCollector(IStatClickCollector):
    """`Must be setted up by:`

    targets (tables name to get data), 
    target file (.db file)
    target time interval ('00:00:00'-'23:59:59' as default)

    _target_file_date is date when file was created (file name without .db). Creates in __init__ automaticaly
    
    With method .get_data() you will recieve dictionary that'll be builded by targets you've set.
    The dict struct is:
    {
        'target': {
            'times': list[str],
            'clicks': list[int]
        }
    }
    """
    _targets: list[str]
    _target_file: str
    _target_file_date: str
    _data_dict: dict
    _target_time_interval: TimeInterval


    def __init__(self, targets: list[str], # Table name
                       target_file: str, # DB File name
                       target_time_interval: TimeInterval = TimeInterval(Time(0, 0, 0), Time(23, 59, 59))) -> None:
        """
        Args:
            from_target (str): Table name\n
            target_date (date): In format: YYYY-MM-DD\n
            target_time_interval (TimeInterval) = ('00:00:00', '23:59:59') | Any\n
        """
        self._targets = targets
        self._target_file = target_file
        self._target_time_interval = target_time_interval
        super().__init__()
        self._prep_data()

    def _prep_data(self):
        """
        1. Initialize dict
        2. Set target
        3. Get data from db
        4. Save data to dict
        5. Go to next target (p. 2)
        """
        self._data_dict = self.init_dict()
        db = ClickCollectorDB(db_name=self._target_file)
        for target in self._targets:
            times, clicks = db.get(target, self._target_time_interval)
            self._data_dict[target]['times'] = times
            self._data_dict[target]['clicks'] = clicks
        del db

    def get_clicks_sum(self, target: str) -> int:
        clicks = sum(self._data_dict[target]['clicks'])
        return clicks

    def get_times(self, target: str) -> list[str]:
        return self._data_dict[target]['times']


class DateStatClickCollector(IStatClickCollector):
    """`Must to be setted up by:`

    targets (tables names to get data), 
    dates interval: start date to end date
    time interval ('00:00:00'-'23:59:59' as default)

    
    With method .get_data() you will recieve dictionary that'll be builded by targets you've set.

    The dict struct is:
    {
        'target': {
            'times': list[str], -- In cause DateStatClickCollector provide data for days -- 'times' is 'days'.
            'clicks': list[int] -- Sum of clicks for a day from dates interval.
        }
    }
    """
    _default_time_interval = TimeInterval(Time(0, 0, 0), Time(23, 59, 59))
    _time_interval: TimeInterval
    _targets: list[str]
    _dates_interval: list[str]
    _data_dict: dict


    def __init__(self, targets: list[str],
                       date_interval: tuple[str, str],
                       time_interval: TimeInterval = _default_time_interval) -> None:
        self._targets = targets
        self._time_interval = time_interval
        self._dates_interval = DateStatClickCollector.prep_dates(date_interval)
        self._prep_data()

    def _prep_data(self):
        """
        1. Initialize dict
        2. Get files names
        3. Set file
        4. Set target
        5. Connect to db file 
        6. Get data from db
        7. Save data to dict
        8. Go to next file (p. 3)
        """
        self._data_dict = self.init_dict()
        files = DateStatClickCollector.prep_dates_to_files(self._dates_interval)
        for file in files:
            for target in self._targets:
                db = ClickCollectorDB(db_name=file)
                _, clicks = db.get(target, self.target_time_interval)
                self._data_dict[target]['times'] = self._dates_interval
                self._data_dict[target]['clicks'] = sum(clicks)
        del db

    @staticmethod
    def prep_dates(date_interval: tuple[str, str]) -> list[str]:
        """
        Args:
            date_interval (tuple[str, str]): Start date to End date of interval

        Returns:
            All dates in interval
        """
        start = datetime.strptime(date_interval[0], '%Y-%m-%d')
        end = datetime.strptime(date_interval[1], '%Y-%m-%d')   

        return [(start + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, (end-start).days)]

    @staticmethod
    def prep_dates_to_files(dates_interval: list[str]) -> list[str]:
        """append `.db` to all dates

        Args:
            dates_interval (list[str]): list of dates in string

        Returns:
            list[str]: list of files in string
        """
        return [date+'.db' for date in dates_interval]