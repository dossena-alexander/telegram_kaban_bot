
class UploadPic():
    def __init__(self, src: str) -> None:
        if src == 'admin':
            self.main_src = 'photos/'
        else:
            self.main_src = 'recieved_photos/'


    def upload(self, file, file_info) -> None:
        src = self.main_src + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(file)



