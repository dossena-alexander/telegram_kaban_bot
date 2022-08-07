from telebot import TeleBot
from telebot import apihelper
from telebot import types

from utils.ban.banned import BannedDB


banned = BannedDB()


class Ban_telebot(TeleBot):
    def get_updates(self, *args, **kwargs):
        json_updates = apihelper.get_updates(self.token, *args, **kwargs)
        ret = []
        banned_users = self._banned_users()
        for update in json_updates:
            if 'message' in update:
                if update['message']['from']['id'] in banned_users:
                    self.last_update_id = update['update_id']
                else:
                    ret.append(types.Update.de_json(update))
            if 'callback_query' in update:
                if update['callback_query']['from']['id'] in banned_users:
                    self.last_update_id = update['update_id']
                else:
                    ret.append(types.Update.de_json(update))
        return ret
        

    
    def _banned_users(self) -> list[int]:
        banned_users = banned.get_users()
        if not banned_users:
            banned_users = [0]

        return banned_users