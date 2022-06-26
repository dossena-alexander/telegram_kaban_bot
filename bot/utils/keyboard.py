from telebot import types


class ReplyKeyboard():
    def __init__(self) -> None:
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)


    def get(self) -> types.ReplyKeyboardMarkup:
        return self.keyboard


    def add(self, keys: list) -> None:
        self._keys = keys
        for button in keys:
            self.keyboard.add(button)


    def autoRow(self) -> None:
        """
        one row -- two buttons
        """
        if len(self._keys) != 0:
            del self.keyboard
            self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            lt = self._keys
            for j in range(len(lt)//2 + len(lt)%2):
                i = j*2
                result = [item for item in lt[i:i+2]]
                a = result[0]
                if len(result) == 2: 
                    b = result[1]
                    self.keyboard.row(a, b)
                else:
                    self.keyboard.row(a)


class InlineKeyboard(): 
    def __init__(self) -> None:
        self.keyboard = types.InlineKeyboardMarkup()


    def get(self) -> types.InlineKeyboardMarkup:
        return self.keyboard


    def add(self, keys: list) -> None:
        """
        keys text is button and callback data
        """
        self._keys = keys
        for text in keys:
            button = types.InlineKeyboardButton(text=text, callback_data=text)
            self.keyboard.add(button)


    def addUrlButton(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self.keyboard.add(button)

    
    def rowUrlButton(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self.keyboard.row(button)


    def autoRow(self) -> None:
        """
        one row -- two buttons
        """
        if len(self._keys) != 0:
            del self.keyboard
            self.keyboard = types.InlineKeyboardMarkup()
            lt = self._keys
            for j in range(len(lt)//2 + len(lt)%2):
                i = j*2
                result = [item for item in lt[i:i+2]]
                a = types.InlineKeyboardButton(text=result[0], callback_data=result[0])
                if len(result) == 2: 
                    b = types.InlineKeyboardButton(text=result[1], callback_data=result[1])
                    self.keyboard.row(a, b)
                else:
                    self.keyboard.row(a)
