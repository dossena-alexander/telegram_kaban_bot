token = ""
adminID = 0

userMsg = "Меню пользователя"
adminMsg = "Админ меню"
helpMsg = "<b>Что я умею</b>\n <i>Мои команды:</i>\n • /start - Запуск\n • /help - Помощь\n • /auth - Аутентификация\n <i>Мои возможности:</i>\n • <b>Какой ты кабан сегодня</b>\n • <b>Фотокарточка</b> –– Смешная картинка\n • <b>Анекдот</b> –– Рандомный анекдот из тысячи"

# keys below will be rowed as you see
# In other words, in one row -- two buttons
# keys is a button text and callback data in the same time

adminKeys = [
         "Картинки",           "Анекдоты",
    "Загрузить картинку", "Загрузить анекдот",
         "Сообщения",          "Рассылка", 
      "Остановить бота", "Пользовательское меню",
          "Добавить кабана", "Статистика"
]

userKeys = [
    "Загрузить картинку", "Загрузить анекдот",
               "Сообщение админу"
]

startKeys = [
    "Анекдот", "Фотокарточка",
    "Какой я кабан сегодня"
]

#limits for user per day
max_jokes_per_day = 10
max_msgs_per_day = 5
max_photos_per_day = 10

#text-worker filter
word_filter = ["Фотокарточка", "Анекдот", "Какой я кабан сегодня"
               "/auth", "/help", "/start"]

#folders
wct_path = '../wct/'
photos_path = '../photos/'
recieved_photos_path = '../recieved_photos/'
db_path = '../db/main.db'
log_path = "../Logs/bot.log"