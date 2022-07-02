from utils.logger import log
from config import PATH

class UploadPic():
    def __init__(self, src: str) -> None:
        if src == 'admin':
            self.main_src = PATH.PHOTOS
        elif src == 'wct':
            self.main_src = PATH.WCT
        else:
            self.main_src = PATH.RECIEVED_PHOTOS


    def upload(self, file, file_info) -> None:
        log.info("UploadPic -- Загрузка файла на сервер")
        src = self.main_src + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(file)
        log.info("Успешно")


