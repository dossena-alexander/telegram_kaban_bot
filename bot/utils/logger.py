from cgitb import handler
from config import PATH
import logging

log = logging.getLogger("bot.py")
log.setLevel(logging.INFO)
fileHandler = logging.FileHandler(PATH.LOG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)
