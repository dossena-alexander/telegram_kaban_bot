from telebot import TeleBot
from telebot import apihelper
from telebot import types

from utils.ban.banned import BannedDB


banned = BannedDB()


class Ban_telebot(TeleBot):
    def get_updates(self, *args, **kwargs):
        json_updates = apihelper.get_updates(self.token, *args, **kwargs)
        ret = []
        for update in json_updates:
            if update['message']['from']['id'] in self._banned_users():
                self.last_update_id = update['update_id']
            else:
                ret.append(types.Update.de_json(update))

        return ret

    
    def _banned_users(self) -> list[int]:
        banned_users = banned.get_users()
        if not banned_users:
            banned_users = [0]

        return banned_users