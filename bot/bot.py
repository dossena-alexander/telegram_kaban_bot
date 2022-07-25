# v1.8.8.2
from handlers import *
from header import *


bot.register_message_handler(commands=["start"], 
                             func=start, 
                             callback="none")

bot.register_message_handler(commands=["auth"], 
                             func=auth, 
                             callback="none")

bot.register_message_handler(commands=["help"], 
                             func=help, 
                             callback="none")

bot.register_message_handler(content_types="text", 
                             func=reply_keyboard_worker, 
                             callback="none")

bot.register_message_handler(content_types="photo", 
                             func=upload_photo_in_private_chat, 
                             callback="none")


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    call_work(call)


if __name__ == "__main__":
    try:
        print("BOT STARTED")
        utils.log.info("BOT STARTED")
        bot.infinity_polling()
    except Exception as e:
        utils.log.error(e)
        bot.send_message(ADMIN_ID, "Bot stoped. Trouble occurred")
