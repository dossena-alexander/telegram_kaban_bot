import time
from config import shedule_path
from utils.logger import log

class Shedule():
    currentShedule = 'None'
    day = ""


    def currentDay(self):
        self.day = time.strftime('%a')
        self.currentShedule = self.day + ".JPG"
        return self.day

    
    def getShedule(self) -> str:
        day = self.currentDay()
        if day == "Sat" or "Sun":
            return shedule_path + "Mon.JPG"
        else:
            return shedule_path + self.currentShedule


