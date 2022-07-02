from utils.keyboard import ReplyKeyboard, InlineKeyboard


class Menu():
    msg = ''

    def __init__(self) -> None:
        self.replyKeyboard = ReplyKeyboard()
        self.inlineKeyboard = InlineKeyboard()


    def setMsg(self, x: str):
        setattr(self, "msg", x)


    def getMsg(self):
        return self.msg
        
    
    def getReplyKeyboard(self):
        return self.replyKeyboard.get()


    def setReplyKeyboard(self, keys: dict):
        self.replyKeyboard.set_keyboard(keys)


    def getInlineKeyboard(self):
        return self.inlineKeyboard.get()


    def setInlineKeyboard(self, keys: dict):
        self.inlineKeyboard.set_keyboard(keys)
