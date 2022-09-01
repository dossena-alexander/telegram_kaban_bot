from PIL import Image, ImageDraw, ImageFont
from server.utils.db import *
from config import PATH


class Image_Statistic():
    def __init__(self) -> None:
        self.path = PATH.MATERIALS+"stats.jpg"
        self.font = ImageFont.truetype(PATH.MATERIALS+'Helvetica.ttc', size=40, index=4)
        self.bold_font = ImageFont.truetype(PATH.MATERIALS+'Helvetica.ttc', size=40, index=1)
        img = Image.new('RGB', (800, 800), (11, 11, 11))
        img.save(self.path)

    def generate(self, val1, val2, val3, val4):
        img = Image.open(self.path)
        idraw = ImageDraw.Draw(img)
        idraw.text((180, 275), '/WCT:\n\n'
                              +'/PHOTO:\n\n'
                              +'/JOKE:\n\n'
                              +'ОТКР. КАБАНОВ:', font=self.font)
        idraw.text((530, 275), f'{val1}\n\n'
                              +f'{val2}\n\n'
                              +f'{val3}\n\n'
                              +f'{val4}', font=self.bold_font)
        img.save(self.path)


class Statistics(DB):
    def __init__(self) -> None:
        super().__init__()
        self.set_table('stats')

    def get(self) -> str:
        self.b    = BoarDB()
        self.p_b  = PremiumBoarDB()
        self.u    = UserDB()
        self.vk_u = UserDB("vk_users", "vk_id")
        self.j    = JokeDB("adminJokes")
        self.p    = PicDB("accPics")

        boars = self.b.get_records_count()
        premium_boars = self.p_b.get_records_count()
        users = self.u.get_records_count()
        vk_users = self.vk_u.get_records_count()
        jokes = self.j.get_records_count()
        photos = self.p.get_records_count()

        txt = (f'<b>Статистика</b>\n'
        + f'• Кабаны: <b>{boars}</b>\n'
        + f'• Премиум кабаны: <b>{premium_boars}</b>\n'
        + f'• Пользователи: <b>{users}</b>\n'
        + f'• ВК Пользователи: <b>{vk_users}</b>\n'
        + f'• Анекдоты: <b>{jokes}</b>\n'
        + f'• Картинки: <b>{photos}</b>\n')
        return txt
    
    def _get_counts(self) -> list[int]:
        cursor = self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        cols = list(map(lambda x: x[0], cursor.description))
        counts = []
        for i in range(len(cols)):
            counts.append(self.get_record(row=0, col=i))

        return counts

    def get_img_stats(self, image_stats: Image_Statistic) -> None:
        counts = self._get_counts()
        image_stats.generate(*counts)

    def update_boar(self) -> None:
        new = self.get_record(row=0, col=0) + 1
        self._bd_cursor.execute(f'UPDATE stats SET boars = {new}')
        self._bd.commit()

    def update_wct(self) -> None:
        new = self.get_record(row=0, col=1) + 1
        self._bd_cursor.execute(f'UPDATE stats SET wct_button = {new}')
        self._bd.commit()

    def update_joke(self) -> None:
        new = self.get_record(row=0, col=2) + 1
        self._bd_cursor.execute(f'UPDATE stats SET joke_button = {new}')
        self._bd.commit()

    def update_photo(self) -> None:
        new = self.get_record(row=0, col=3) + 1
        self._bd_cursor.execute(f'UPDATE stats SET photo_button = {new}')
        self._bd.commit()



img_s = Image_Statistic()
img_s.generate(20, 30, 40 ,50)