from telebot import types


class Keyboard():
    def __init__(self) -> None:
        self._keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    def get(self):
        pass

    def set(self, keys: dict) -> None:
        pass


class ReplyKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()

    def get(self) -> types.ReplyKeyboardMarkup:
        return self._keyboard

    def set(self, keys: dict) -> None:
        """        
        Keys as dictionary is rowing in two buttons grid.
        The parametred dict will used to set it up to tuples list for further rowing.

        Args:
            keys (dict): in form -> dict = {0: "text": "button-text", "call": "button-call-text"}
        """
        buttons_as_listed_tuples = []

        for button in keys.values():
            buttons_as_listed_tuples.append(button["text"])

        self._row_buttons(buttons_as_listed_tuples)

    def _row_buttons(self, buttons):
        for j in range(len(buttons)//2 + len(buttons)%2):
            i = j*2
            result = [item for item in buttons[i:i+2]]
            a = result[0]
            if len(result) == 2: 
                b = result[1]
                self._keyboard.row(a, b)
            else:
                self._keyboard.row(a)

    def add_button(self, text) -> None:
        self._keyboard.add(text)


class InlineKeyboard(Keyboard): 
    def __init__(self) -> None:
        super().__init__()
        
    def get(self) -> types.InlineKeyboardMarkup:
        return self._keyboard

    def set(self, keys: dict) -> None:
        """        
        Keys as dictionary is rowing in two buttons grid.
        The parametred dict will used to set it up to tuples list for further rowing.

        Args:
            keys (dict): in form -> dict = {0: "text": "button-text", "call": "button-call-text"}
        """
        buttons_as_listed_tuples = []

        for button in keys.values():
            buttons_as_listed_tuples.append((button["text"], button["call"]))
            
        self._row_buttons(buttons_as_listed_tuples)

    def _row_buttons(self, buttons):
        for j in range(len(buttons)//2 + len(buttons)%2):
            i = j*2
            result = [item for item in buttons[i:i+2]]
            a = types.InlineKeyboardButton(text=result[0][0], callback_data=result[0][1])
            if len(result) == 2: 
                b = types.InlineKeyboardButton(text=result[1][0], callback_data=result[1][1])
                self._keyboard.row(a, b)
            else:
                self._keyboard.row(a)

    def add_url_button(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self._keyboard.add(button)

    def add_button(self, text: str, call: str) -> None:
        button = types.InlineKeyboardButton(text=text, callback_data=call)
        self._keyboard.add(button)
