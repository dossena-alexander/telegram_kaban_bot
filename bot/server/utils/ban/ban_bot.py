from typing import Union, Optional
from telebot import TeleBot
from telebot import apihelper
from telebot import types
from telebot import REPLY_MARKUP_TYPES

from server.utils import UserDB
from server.utils.ban.banned import BannedDB


banned = BannedDB()


class Ban_telebot(TeleBot):
    def __init__(self, token, parse_mode=None, threaded=True, skip_pending=False, num_threads=2, next_step_backend=None, reply_backend=None, exception_handler=None, last_update_id=0, suppress_middleware_excepions=False, state_storage=...):
        super().__init__(token, parse_mode, threaded, skip_pending, num_threads, next_step_backend, reply_backend, exception_handler, last_update_id, suppress_middleware_excepions, state_storage)
        self.userDB = UserDB()

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
            elif 'callback_query' in update:
                if update['callback_query']['from']['id'] in banned_users:
                    self.last_update_id = update['update_id']
                else:
                    ret.append(types.Update.de_json(update)) 
            else:
                ret.append(types.Update.de_json(update))     
        return ret

    def send_notification(
            self, chat_id: Union[int, str], text: str, 
            parse_mode: Optional[str]=None, 
            entities: Optional[list[types.MessageEntity]]=None,
            disable_web_page_preview: Optional[bool]=None, 
            disable_notification: Optional[bool]=None, 
            protect_content: Optional[bool]=None,
            reply_to_message_id: Optional[int]=None, 
            allow_sending_without_reply: Optional[bool]=None,
            reply_markup: Optional[REPLY_MARKUP_TYPES]=None,
            timeout: Optional[int]=None) -> types.Message:
        can_send = self.userDB.can_send_notification(int(chat_id))
        if can_send:
            self.send_message(
                chat_id, text, 
                parse_mode, 
                entities,
                disable_web_page_preview, 
                disable_notification, 
                protect_content,
                reply_to_message_id, 
                allow_sending_without_reply,
                reply_markup,
                timeout)
        
    def send_photo_notification(
            self, chat_id: Union[int, str], photo: Union[any, str], 
            caption: Optional[str]=None, parse_mode: Optional[str]=None,
            caption_entities: Optional[list[types.MessageEntity]]=None,
            disable_notification: Optional[bool]=None,
            protect_content: Optional[bool]=None,
            reply_to_message_id: Optional[int]=None, 
            allow_sending_without_reply: Optional[bool]=None,
            reply_markup: Optional[REPLY_MARKUP_TYPES]=None,
            timeout: Optional[int]=None,) -> types.Message:
        can_send = self.userDB.can_send_notification(int(chat_id))
        if can_send:
            self.send_message(
                chat_id, photo, 
                caption, parse_mode,
                caption_entities,
                disable_notification,
                protect_content,
                reply_to_message_id, 
                allow_sending_without_reply,
                reply_markup,
                timeout)


    def _banned_users(self) -> list[int]:
        banned_users = banned.get_users()
        if not banned_users:
            banned_users = [0]

        return banned_users