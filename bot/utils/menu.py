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

    
    def setReplyKeyboard(self, keys: list):
        self.replyKeyboard.add(keys)


    def getInlineKeyboard(self):
        return self.inlineKeyboard.get()


    def setInlineKeyboard(self, keys: list):
        self.inlineKeyboard.add(keys)


    def rowInlineKeyboard(self):
        self.inlineKeyboard.autoRow()


    def rowReplyKeyboard(self):
        self.replyKeyboard.autoRow()