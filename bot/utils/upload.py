import imp
from logger import log


class UploadPic():
    def __init__(self, src: str) -> None:
        if src == 'admin':
            self.main_src = 'photos/'
        elif src == 'wct':
            self.main_src = 'wct/'
        else:
            self.main_src = 'recieved_photos/'


    def upload(self, file, file_info) -> None:
        log.info("UploadPic -- Загрузка файла на сервер")
        src = self.main_src + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(file)
        log.info("Успешно")


