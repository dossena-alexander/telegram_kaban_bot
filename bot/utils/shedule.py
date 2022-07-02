import time
from config import PATH
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
            return open(PATH.SHEDULE + "Mon.JPG", 'rb')
        else:
            return open(PATH.SHEDULE + self.currentShedule, 'rb')


