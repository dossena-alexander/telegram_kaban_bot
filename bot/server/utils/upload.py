from server.utils.logger import log
from config import UPLOAD_LOCK


class UploadPic():
    __src: str 


    def __init__(self, src: str) -> None:
        self.__src = src

    def upload(self, file, file_name) -> None:
        """Upload only photo
        """
        if not UPLOAD_LOCK:
            try:
                source_file_name = self.__src + file_name
                with open(source_file_name, 'wb') as new_file:
                    new_file.write(file)
            except:
                log.error("UploadPic -- Загрузка файла на сервер")


