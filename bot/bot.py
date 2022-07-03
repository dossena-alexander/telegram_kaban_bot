# v1.8.3
from handlers import *
from header import *


bot.register_message_handler(commands=["start"], func=start, callback="none")
bot.register_message_handler(commands=["auth"], func=auth, callback="none")
bot.register_message_handler(commands=["help"], func=help, callback="none")
bot.register_message_handler(content_types="text", func=textWorker, callback="none")


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    callWorker(call)


if __name__ == "__main__":
    try:
        print("BOT STARTED")
        utils.log.info("BOT STARTED")
        bot.polling()
    except Exception as e:
        utils.log.error(e)
        bot.send_message(ADMIN_ID, "Bot stoped. Trouble occurred")
        # you may use bot.polling() or sh script to restart bot.py
        # for sh script use:
        # import subprocess
        # proc = subprocess.Popen('./your_sh.sh', stdout=subprocess.PIPE)
        # output = proc.stdout.read()