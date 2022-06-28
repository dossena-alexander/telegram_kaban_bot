token = ""
adminID = 0
#========================MSG===================================

userMsg = "Меню пользователя"
adminMsg = "Админ меню"
helpMsg = "<b>Что я умею</b>\n <i>Мои команды:</i>\n • /start - Запуск\n • /help - Помощь\n • /auth - Аутентификация\n <i>Мои возможности:</i>\n • <b>Какой ты кабан сегодня</b>\n • <b>Фотокарточка</b> –– Смешная картинка\n • <b>Анекдот</b> –– Рандомный анекдот из тысячи"
userSubMenuMsg = "Кабаний перевод телеграмм для настоящих кабанов, просто нажми на кнопку, чтобы установить"

#========================KEYS===================================

# keys below will be rowed as you see
# In other words, in one row -- two buttons
# keys is a button text and callback data in the same time

adminKeys = [
        "Предложения",         "Загрузка",
         "Сообщения",          "Рассылка", 
      "Остановить бота",     "Пользователь",
                    "Статистика"
]

userKeys = [
        "Загрузить", "Сообщение админу",
          "Кабаний перевод телеграмм"
]

startKeys = [
    "Анекдот", "Фотокарточка",
    "Какой я кабан сегодня", "Расписание"
]

#========================LIMITS===================================

#limits for user per day
max_jokes_per_day = 10
max_msgs_per_day = 5
max_photos_per_day = 10

#========================FILTER===================================

#text-worker filter
word_filter = ["Фотокарточка", "Анекдот", "Какой я кабан сегодня", "Расписание"
               "/auth", "/help", "/start"]

#========================PATHS===================================

#folders
wct_path = '../wct/'
photos_path = '../photos/'
recieved_photos_path = '../recieved_photos/'
db_path = '../db/main.db'
log_path = "../Logs/bot.log"
shedule_path = "../Shedule/"

#===========================================================