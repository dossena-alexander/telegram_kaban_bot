from cgitb import handler
import logging

log = logging.getLogger("bot.py")
log.setLevel(logging.INFO)
fileHandler = logging.FileHandler("../Logs/bot.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)
