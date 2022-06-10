import telebot, random, bd
import menu
from logger import *
from config import *
from upload import *
from keyboard import *


# from dialog import Dialog

# from shedule import Shed

bot = telebot.TeleBot(token=token)
msgCounter = 0 # records counter that`s used to see user msgs in admin menu
userBD = bd.UserBD()
jokeBD = bd.JokeBD()
msgBD = bd.MsgBD()
picBD = bd.PicBD()
adminMenu = menu.Menu()
userMenu = menu.Menu()
helpMenu = menu.Menu()


# soon...
# shed = Shed()
# dialog = Dialog()



# keys below will be rowed as you see
# In other words, in one row -- two buttons
# keys is a button text and callback data in the same time

adminKeys = [
         "Картинки",           "Анекдоты",
    "Загрузить картинку", "Загрузить анекдот",
         "Сообщения",          "Рассылка", 
      "Остановить бота", "Пользовательское меню"
]

userKeys = [
    "Загрузить картинку", "Загрузить анекдот",
               "Сообщение админу"
]

helpMenu.setMsg("") #!!!
adminMenu.setMsg("Админ меню")
adminMenu.setInlineKeyboard(adminKeys)
adminMenu.rowInlineKeyboard()
userMenu.setMsg("Меню пользователя")
userMenu.setInlineKeyboard(userKeys)
userMenu.rowInlineKeyboard()


@bot.message_handler(commands=["start"])
def start(message):
    keys = [
        "Анекдот",
        "Фотокарточка",
        "Какой ты кабан сегодня"
    ]
    keyboard = ReplyKeyboard()
    keyboard.add(keys)
    keyboard.autoRow()
    bot.send_message(message.chat.id, "Вечер в хату, кабан {0.first_name}!"
        .format(message.from_user, bot.get_me()), reply_markup=keyboard.get())


@bot.message_handler(commands=["auth"])
def auth(message):
    global adminID

    # as long as ...user.id is integer, userID get it in string to be recorded to DB (column has string type)
    userID = str(message.from_user.id) 
    if userID == str(adminID):
        admin(message)
    else:
        usersList = userBD.getUsersList()
        if userID not in usersList:
            log.info("Auth -- Добавление пользователя в БД")
            userBD.addUser(userID)
            log.info("      Успешно")
            user(message)
        else:
            user(message)


def admin(message):
    bot.send_message(message.chat.id, adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard())


def user(message):
    bot.send_message(message.chat.id, userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard()) 


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, helpMenu.getMsg())


@bot.callback_query_handler(func=lambda call: True)
def callWorker(call):
    global msgCounter 
    global jokes
    global msgs

    if call.data == 'Загрузить картинку': #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Пришли картинку, или напиши 'отмена'", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadPicture)
    elif call.data == 'Загрузить анекдот': #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Напиши анекдот, или напиши 'отмена'", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadJoke)
    # elif call.data == "back":
    #     if id == adminID: 
    #         bot.edit_message_text(call.message.chat.id, call.message.message_id, text=adminMenu.getMsg(), reply_markup=adminMenu.getInlineKeyboard())
    #     else: 
    #         bot.edit_message_text(call.message.chat.id, call.message.message_id, text=userMenu.getMsg(), reply_markup=userMenu.getInlineKeyboard())
    elif call.data == "Остановить бота": #+
        bot.answer_callback_query(call.id, 'Бот остановлен')
        log.info("ОСТАНОВКА БОТА")
        bot.stop_polling()
    elif call.data == "Анекдоты": #+
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        jokes = jokeBD.getAllJokes()
        see_jokes(call.message)
    elif call.data == "Выйти": #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text=adminMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.getInlineKeyboard())
    elif call.data == "Далее": #joke
        msgCounter += 1
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_jokes(call.message)
    elif call.data == "Далее>>": #msg
        msgCounter += 1
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        seeMsgs(call.message)
    elif call.data == "Принять": #joke
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        jokeBD.setTableName("adminJokes")
        jokeBD.newRecord(jokeBD.getTableName(), jokeBD.getColName(), jokeBD.seeJoke(msgCounter))
        msgCounter += 1
        see_jokes(call.message)
    elif call.data == "Удалить": #joke
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        jokeBD.setTableName("userJokes")
        jokeBD.delRecord(jokeBD.getTableName(), jokeBD.getColName(), jokeBD.seeJoke(msgCounter))
        msgCounter = 0
        see_jokes(call.message)
    elif call.data == "Вычеркнуть": #msg
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msgBD.delRecord(msgBD.getTableName(), msgBD.getColName(), msgBD.seeMsg(msgCounter))
        msgCounter = 0
        seeMsgs(call.message)
    elif call.data == "Рассылка": #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Напиши сообщение пользователям", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, notify)
    elif call.data == "Пользовательское меню": #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text=userMenu.getMsg(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.getInlineKeyboard())
    elif call.data == "Сообщения":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msgs = msgBD.getAllMsgs()
        seeMsgs(call.message)
    elif call.data == "Картинки":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        seePics(call.message)



def see_jokes(message):
    global msgCounter
    
    stand_keys = [
        "Выйти", "Далее",
        "Принять","Удалить"
    ]

    back_key = ["Выйти"]

    stand_keyboard = InlineKeyboard()
    stand_keyboard.add(stand_keys)
    stand_keyboard.autoRow()
    back_keyboard = InlineKeyboard()
    back_keyboard.add(back_key)

    # get records len with jokeBD method
    record_len = jokeBD.getRecCount("userJokes")
    if record_len != 0:
        if msgCounter < record_len: # msgCounter is counter which increase and count every each record 
            bot.send_message(message.chat.id,
                f"{record_len} записей\n" +
                f"{jokeBD.seeJoke(recNum=msgCounter)}",
                reply_markup=stand_keyboard.get())
        else:
            msgCounter = 0
            bot.send_message(
                message.chat.id,
                "Анекдоты кончились",
                reply_markup=back_keyboard.get())
    else:
        bot.send_message(message.chat.id, "Анекдотов нет", reply_markup=back_keyboard.get())


def seePics(message):
    pass


def seeMsgs(message):
    global msgCounter

    stand_keys = [
        "Выйти", "Далее>>",
            "Вычеркнуть"
    ]

    back_key = ["Выйти"]

    stand_keyboard = InlineKeyboard()
    stand_keyboard.add(stand_keys)
    stand_keyboard.autoRow()
    back_keyboard = InlineKeyboard()
    back_keyboard.add(back_key)

    # get records len with msgBD method
    record_len = msgBD.getRecCount("msgs")
    if record_len != 0:
        if msgCounter < record_len: # msgCounter is counter which increase and count every each record 
            bot.send_message(message.chat.id,
                f"{record_len} записей\n" +
                f"{msgBD.seeMsg(recNum=msgCounter)}",
                reply_markup=stand_keyboard.get())
        else:
            msgCounter = 0
            bot.send_message(
                message.chat.id,
                "Сообщения кончились",
                reply_markup=back_keyboard.get())
    else:
        bot.send_message(message.chat.id, "Сообщений нет", reply_markup=back_keyboard.get())


def notify(message):
    msg = message.text
    users = userBD.getUsersList()
    if len(users) != 0:
        for i in users:
            bot.send_message(i[0], 
            "<b>Сообщение от админа:</b>\n" + msg, parse_mode="html")
    else:
        bot.send_message(adminID, "Пользователей для рассылки нет")


def uploadPicture(message): #+
    global adminID

    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadPicture)
        else:
            id = message.from_user.id
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            if id == adminID: upPic = UploadPic('admin'); txt = "Сохранил"; picBD.setTableName("accPics")
            # uploadPic('admin') is saving pics to main -- "photos/"; picBD saving photo id to accepted pics table
            else: upPic = UploadPic('user'); txt = "Добавлено на рассмотрение"; picBD.setTableName("pics")
            log.info("UploadPicture -- Загрузка файла")
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            log.info("                  Успешно")
            file = bot.download_file(file_info.file_path)
            # saving photo id to DB of pics, either accepted pics table or pics table
            log.info("                 Запись в БД")
            picBD.newRecord(picBD.getTableName(), picBD.getColName(), file_info.file_path.replace('photos/', ''))
            log.info("                  Успешно")
            log.info("                 Загрузка файла на сервер")
            upPic.upload(file, file_info)
            log.info("                  Успешно")
            bot.send_message(message.chat.id, txt)
    else:
        if message.content_type == "text":
            if message.text.lower() == "отмена":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка!")
                bot.register_next_step_handler(message, uploadPicture)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка!")
            bot.register_next_step_handler(message, uploadPicture)


def uploadJoke(message): #+
    global adminID
    if message.content_type == "text":
        if message.text.lower() != "отмена":
            joke = message.text
            id = message.from_user.id 
            if id == adminID: jokeBD.setTableName('adminJokes'); txt = "Сохранил"
            else: jokeBD.setTableName('userJokes'); txt = "Добавлено на рассмотрение"
            log.info("uploadJoke -- Запись шутки в БД")
            jokeBD.newRecord(jokeBD.getTableName(), jokeBD.getColName(), joke)
            log.info("                 Успешно")
            bot.send_message(message.chat.id, txt)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Только текст!")
        bot.register_next_step_handler(message, uploadJoke)


def getWct(message):
    pass
    # WCT is Which Caban (boar) you Today is
    # every day user changes his "board id"
    # if user in one day, when he used function in bot, will use wct again, wct give the same "boar id"
    
    # photo_folder = './wct/'
    # id = message.from_user.id 
    # users = userBD.getUsersList()
    # if id not in users:
    #     random_file=random.choice(os.listdir(photo_folder))
    #     return open(photo_folder + random_file, 'rb')
    # else:
    #     bot.send_photo(message.chat.id, open(photo_folder + Users_ids[message.from_user.id], 'rb'))


@bot.message_handler(content_types="text") #+
def textWorker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        bot.send_photo(message.chat.id, 
        open("./photos/" + picBD.getPicID(recNum=random.randint(0, picBD.getRecCount("accPics") - 1)), "rb"))
    elif msg == "анекдот":
        bot.send_message(message.chat.id, 
        jokeBD.getJoke(recNum=random.randint(0, jokeBD.getRecCount("adminJokes") - 1)))
    elif msg == "какой ты кабан сегодня":
        bot.send_photo(message.chat.id, getWct())

