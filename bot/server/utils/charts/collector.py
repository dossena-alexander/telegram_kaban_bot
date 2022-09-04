import sqlite3
from datetime import date, datetime, timedelta
from config import PATH
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
    new_time: Time


    def __init__(self) -> None:
        date = datetime.now()
        self.hour = date.hour
        self.time = Time(date.time().strftime('%H:%M:%S'))

    def new_hour(self) -> bool:
        if self.same_hour():
            return False
        return True

    def get_time(self) -> str:
        return self.time

    def same_hour(self) -> bool:
        date = datetime.now()
        now_hour = date.hour
        if now_hour > self.hour:
            self.time = Time(date.time().strftime('%H:%M:%S'))
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
        self.db = sqlite3.connect(PATH.DB_STATS+db_name, check_same_thread=False)
        self.db_cursor = self.db.cursor()

    def create(self):
        self.db_cursor.execute('CREATE TABLE wct_clicks (time TIME, clicks INTEGER)') 
        self.db.commit()
        self.db_cursor.execute('CREATE TABLE photo_clicks (time TIME, clicks INTEGER)') 
        self.db.commit()
        self.db_cursor.execute('CREATE TABLE joke_clicks (time TIME, clicks INTEGER)') 
        self.db.commit()

    def set_date(self, date: date) -> None:
        self.date = date

    @lock_thread
    def insert(self, name: str, time: Time, clicks: int):
        try:
            time = str(time)
            self.db_cursor.execute(f'INSERT INTO {name} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
        except Exception as e:
            self.create()
            self.db_cursor.execute(f'INSERT INTO {name} (time, clicks) VALUES (?, ?)', (time, clicks) ) 
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

    def _now_day(self, full_date = False) -> int:
        now = date.today() # yyyy-mm-dd
        if full_date:
            return now
        return now.day

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
        self.target = target
        self.observer = ClickCollectorObserver()
        self.db = ClickCollectorDB()
        self.clicks = 0

    def new(self) -> None:
        self.clicks += 1
        if self.observer.new_hour():
            time = self.observer.get_time()
            self.db.insert(self.target, time, self.clicks)
            self.clicks = 0


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
        if not self.clicks:
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
                       date_interval: tuple([datetime, datetime]),
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
