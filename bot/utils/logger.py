from cgitb import handler
import config
import logging

log = logging.getLogger("bot.py")
log.setLevel(logging.INFO)
fileHandler = logging.FileHandler(config.log_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)
