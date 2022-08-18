from utils.keyboard import ReplyKeyboard, InlineKeyboard


class Menu():
    msg = ''

    def __init__(self) -> None:
        self.replyKeyboard = ReplyKeyboard()
        self.inlineKeyboard = InlineKeyboard()


    def set_message(self, x: str):
        setattr(self, "msg", x)

    @property
    def message(self):
        return self.msg
        
    
    def get_reply_keyboard(self):
        return self.replyKeyboard.get()


    def set_reply_keyboard(self, keys: dict):
        self.replyKeyboard.set(keys)


    def get_inline_keyboard(self):
        return self.inlineKeyboard.get()


    def set_inline_keyboard(self, keys: dict):
        self.inlineKeyboard.set(keys)
