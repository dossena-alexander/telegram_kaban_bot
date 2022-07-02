from telebot import types


class ReplyKeyboard():
    def __init__(self) -> None:
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)


    def get(self) -> types.ReplyKeyboardMarkup:
        return self.keyboard


    def set_keyboard(self, keys: dict) -> None:
        """
        Keys as dictionary is rowing in two buttons grid.
        The parametred dict will used to set it up to tuples list for further rowing.
        """
        buttons_as_listed_tuples = []

        for item in keys.values():
            buttons_as_listed_tuples.append(item["text"])

        lt = buttons_as_listed_tuples
        for j in range(len(lt)//2 + len(lt)%2):
            i = j*2
            result = [item for item in lt[i:i+2]]
            a = result[0]
            if len(result) == 2: 
                b = result[1]
                self.keyboard.row(a, b)
            else:
                self.keyboard.row(a)


    def add_button(self, text) -> None:
        self.keyboard.add(text)


class InlineKeyboard(): 
    def __init__(self) -> None:
        self.keyboard = types.InlineKeyboardMarkup()


    def get(self) -> types.InlineKeyboardMarkup:
        return self.keyboard


    def set_keyboard(self, keys: dict) -> None:
        """
        Keys as dictionary is rowing in two buttons grid.
        The parametred dict will used to set it up to tuples list for further rowing.
        """
        buttons_as_listed_tuples = []

        for item in keys.values():
            buttons_as_listed_tuples.append((item["text"], item["call"]))

        lt = buttons_as_listed_tuples
        for j in range(len(lt)//2 + len(lt)%2):
            i = j*2
            result = [item for item in lt[i:i+2]]
            a = types.InlineKeyboardButton(text=result[0][0], callback_data=result[0][1])
            if len(result) == 2: 
                b = types.InlineKeyboardButton(text=result[1][0], callback_data=result[1][1])
                self.keyboard.row(a, b)
            else:
                self.keyboard.row(a)


    def add_url_button(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self.keyboard.add(button)

    
    def row_url_button(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self.keyboard.row(button)


    def add_button(self, text: str, call: str) -> None:
        button = types.InlineKeyboardButton(text=text, callback_data=call)
        self.keyboard.add(button)


    # def row_button(self, text: str, call: str) -> None:
    #     button = types.InlineKeyboardButton(text=text, callback_data=call)
    #     self.keyboard.row(button)