import telebot, random, db
import menu
import os
from logger import *
from config import *
from upload import *
from keyboard import *
from datetime import datetime, date

# from dialog import Dialog

# from shedule import Shed

bot = telebot.TeleBot(token=token)
msgCounter = 0 # records counter that`s used to see user msgs in admin menu
userDB = db.UserDB()
boarDB = db.BoarDB()
jokeDB = db.JokeDB()
msgDB = db.MsgDB()
picDB = db.PicDB()
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
      "Остановить бота", "Пользовательское меню",
                "Добавить кабана"
]

userKeys = [
    "Загрузить картинку", "Загрузить анекдот",
               "Сообщение админу"
]

helpMenu.setMsg(
    "<b>Что я умею</b>:\n" +
		" <i>Мои команды:</i>\n" +
		" • /start - запуск\n" +
		" • /auth - Аутентификация пользователя\n" +
        " <i>Мои возможности:</i>\n" +
        " • Какой ты кабан сегодня\n" +
        " • Фотокарточка -- рандомная смешная картинка" +
        " • Анекдот -- рандомный анекдот из более чем тысячной базы данных")
adminMenu.setMsg("Админ меню")
adminMenu.setInlineKeyboard(adminKeys)
adminMenu.rowInlineKeyboard()
userMenu.setMsg("Меню пользователя")
userMenu.setInlineKeyboard(userKeys)
userMenu.rowInlineKeyboard()


@bot.message_handler(commands=["start"])
def start(message):
    keys = [
        "Анекдот", "Фотокарточка",
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
        usersList = userDB.getUsersList()
        if userID not in usersList:
            log.info("Auth -- Добавление пользователя в БД")
            userDB.addUser(userID)
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
    bot.send_message(message.chat.id, helpMenu.getMsg(), parse_mode="html")


@bot.callback_query_handler(func=lambda call: True)
def callWorker(call):
    global msgCounter 
    global jokes

    if call.data == 'Загрузить картинку': #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadPicture)
    elif call.data == 'Загрузить анекдот': #+
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadJoke)
    elif call.data == "Остановить бота": #+
        bot.answer_callback_query(call.id, 'Бот остановлен')
        log.info("ОСТАНОВКА БОТА")
        bot.stop_polling()
    elif call.data == "Анекдоты": #+
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
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
        jokeDB.setTableName("adminJokes")
        jokeDB.newRecord(jokeDB.getTableName(), jokeDB.getColName(), jokeDB.seeJoke(msgCounter))
        msgCounter += 1
        see_jokes(call.message)
    elif call.data == "Удалить": #joke
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        jokeDB.setTableName("userJokes")
        jokeDB.delRecord(jokeDB.getTableName(), jokeDB.getColName(), jokeDB.seeJoke(msgCounter))
        msgCounter = 0
        see_jokes(call.message)
    elif call.data == "Вычеркнуть": #msg
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msgDB.delRecord(msgDB.getTableName(), msgDB.getColName(), msgDB.seeMsg(msgCounter))
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
        seeMsgs(call.message)
    elif call.data == "Картинки":
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        seePics(call.message)
    elif call.data == "Сообщение админу":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Напиши сообщение или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadMsg)
    elif call.data == "Добавить кабана":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, uploadWct)

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

    # get records len with jokeDB method
    record_len = jokeDB.getRecCount("userJokes")
    if record_len != 0:
        if msgCounter < record_len: # msgCounter is counter which increase and count every each record 
            bot.send_message(message.chat.id,
                f"{record_len} записей\n" +
                f"{jokeDB.seeJoke(recNum=msgCounter)}",
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

    # get records len with msgDB method
    record_len = msgDB.getRecCount("msgs")
    if record_len != 0:
        if msgCounter < record_len: # msgCounter is counter which increase and count every each record 
            bot.send_message(message.chat.id,
                f"{record_len} записей\n" +
                f"{msgDB.seeMsg(recNum=msgCounter)}",
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
    users = userDB.getUsersList()
    if len(users) != 0:
        for i in users:
            bot.send_message(i[0], 
            "<b>Сообщение от админа:</b>\n" + msg, parse_mode="html")
    else:
        bot.send_message(adminID, "Пользователей для рассылки нет")


def uploadPicture(message): 
    global adminID

    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadPicture)
        else:
            id = message.from_user.id
            # Checking ID of user, if admin is adding, pics`ll be added to main folder "photos/
            # if not, bot send photo id to DB, after all admin`ll be able to save pics to "photos/
            if id == adminID: upPic = UploadPic('admin'); txt = "Сохранил"; picDB.setTableName("accPics")
            # uploadPic('admin') is saving pics to main -- "photos/"; picDB saving photo id to accepted pics table
            else: upPic = UploadPic('user'); txt = "Добавлено на рассмотрение"; picDB.setTableName("pics")
            log.info("UploadPicture -- Загрузка файла")
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            log.info("                  Успешно")
            file = bot.download_file(file_info.file_path)
            # saving photo id to DB of pics, either accepted pics table or pics table
            log.info("                 Запись в БД")
            picDB.newRecord(picDB.getTableName(), picDB.getColName(), file_info.file_path.replace('photos/', ''))
            log.info("                  Успешно")
            log.info("                 Загрузка файла на сервер")
            upPic.upload(file, file_info)
            log.info("                  Успешно")
            bot.send_message(message.chat.id, txt)
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка!")
                bot.register_next_step_handler(message, uploadPicture)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка!")
            bot.register_next_step_handler(message, uploadPicture)


def uploadJoke(message):
    global adminID

    if message.content_type == "text":
        if message.text.lower() != "/brake":
            joke = message.text
            id = message.from_user.id 
            if id == adminID: jokeDB.setTableName('adminJokes'); txt = "Сохранил"
            else: jokeDB.setTableName('userJokes'); txt = "Добавлено на рассмотрение"
            log.info("uploadJoke -- Запись шутки в БД")
            jokeDB.newRecord(jokeDB.getTableName(), jokeDB.getColName(), joke)
            log.info("                 Успешно")
            bot.send_message(message.chat.id, txt)
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Только текст, пиши или нажми /brake")
        bot.register_next_step_handler(message, uploadJoke)


def uploadMsg(message): #+-
    global adminID

    if message.content_type == "text":
        if message.text.lower() != "/brake":
            msg = message.text
            log.info("uploadMsg -- Запись сообщения в БД")
            msgDB.newRecord(msgDB.getTableName(), msgDB.getColName(), msg)
            log.info("                 Успешно")
            bot.send_message(message.chat.id, "Отправлено")
        else:
            bot.send_message(message.chat.id, "Отменено")
    else:
        bot.send_message(message.chat.id, "Только текст, пиши или нажми /brake")
        bot.register_next_step_handler(message, uploadJoke)


def uploadWct(message):
    if message.content_type == 'photo':
        if message.content_type == "media_group": # able to save not only one pic
            bot.send_message(message.chat.id, "Пришли только одну картинку")
            bot.register_next_step_handler(message, uploadWct)
        else:
            upPic = UploadPic('wct')
            log.info("UploadWct -- Загрузка файла")
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            log.info("                  Успешно")
            file = bot.download_file(file_info.file_path)
            log.info("                 Запись в БД")
            boarDB.newRecord(boarDB.getTableName(), boarDB.getColName(), file_info.file_path.replace('photos/', ''))
            log.info("                  Успешно")
            log.info("                 Загрузка файла на сервер")
            upPic.upload(file, file_info)
            log.info("                  Успешно")
            bot.send_message(message.chat.id, "Сохранил")
    else:
        if message.content_type == "text":
            if message.text.lower() == "/brake":
                bot.send_message(message.chat.id, "Отменено")  
            else:
                bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
                bot.register_next_step_handler(message, uploadWct)    
        else:      
            bot.send_message(message.chat.id, "Это не картинка, пришли фото или жми /brake")
            bot.register_next_step_handler(message, uploadWct)


def getWct(message):
    global adminID

#     # WCT is "Which Caban (boar) you Today is"
#     # every day user changes his "board id"
#     # if user in one day, when he used function in bot, will use wct again, wct give the same "boar id"
    
    photo_folder = './wct/'
    id = message.from_user.id 
    users = userDB.getUsersList()
    if id != adminID and id not in users:
        bot.send_message(message.chat.id, "Ты не зарегистрировался. Нажми /auth, чтобы зарегистрироваться")
        return None
    else:
        now = date.today()
        now_day = now.day
        prev_day = userDB.getPrevDay(id)
        if now_day == prev_day:
            boarID = userDB.getWctForUser(id)
            boar = boarDB.getID(boarID)
            return open(photo_folder + boar, 'rb')
        else:
            userDB.setPrevDay(now_day, id)
            boarID = random.randint(0, boarDB.getRecCount( boarDB.getTableName() ) - 1)
            userDB.setWctForUser(id, boarID)
            boar = boarDB.getID(boarID)
            return open(photo_folder + boar, 'rb')


@bot.message_handler(content_types="text") #+
def textWorker(message):
    msg = message.text.lower()
    if msg == "фотокарточка":
        bot.send_photo(message.chat.id, 
        open("./photos/" + picDB.getPicID(recNum=random.randint(0, picDB.getRecCount("accPics") - 1)), "rb"))
    elif msg == "анекдот":
        bot.send_message(message.chat.id, 
        jokeDB.getJoke(recNum=random.randint(0, jokeDB.getRecCount("adminJokes") - 1)))
    elif msg == "какой ты кабан сегодня":
        if getWct(message) != None:
            bot.send_photo(message.chat.id, getWct(message))

