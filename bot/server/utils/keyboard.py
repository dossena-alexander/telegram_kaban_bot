from telebot import types


class ReplyKeyboard(types.ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=True, row_width=1, selective=False) -> None:
        super().__init__(resize_keyboard=resize_keyboard,
                         row_width=row_width,
                         selective=selective)

    def get(self) -> types.ReplyKeyboardMarkup:
        return self

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
                self.row(a, b)
            else:
                self.row(a)

    def add_button(self, text) -> None:
        self.add(text)


class InlineKeyboard(types.InlineKeyboardMarkup): 
    def get(self) -> types.InlineKeyboardMarkup:
        return self

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
                self.row(a, b)
            else:
                self.row(a)

    def add_url_button(self, key: str, url: str) -> None:
        button = types.InlineKeyboardButton(text=key, url=url)
        self.add(button)

    def add_button(self, text: str, call: str) -> None:
        button = types.InlineKeyboardButton(text=text, callback_data=call)
        self.add(button)


def build_buttons(keys: dict):
    """Build inline telegram buttons from dict such as: \n
    {
        0: 'text': 'some_text', 'call': 'some_call',
        1: 'text': 'some_text', 'call': 'some_call'
    }

    Args:
        keys (dict): _description_

    Returns:
        List of types.InlineKeyboardButton
    """
    buttons = []
    for button in keys.values():
        inlineButton = types.InlineKeyboardButton(text=button["text"], callback_data=button["call"])
        buttons.append(inlineButton)
        
    return buttons