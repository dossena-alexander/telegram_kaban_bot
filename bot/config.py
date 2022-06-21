token = ""
adminID = 0

userMsg = "Меню пользователя"
adminMsg = "Админ меню"
helpMsg = "<b>Что я умею</b>:\n <i>Мои команды:</i>\n • /start - запуск\n • /auth - Аутентификация пользователя\n <i>Мои возможности:</i>\n • Какой ты кабан сегодня\n • Фотокарточка -- рандомная смешная картинка • Анекдот -- рандомный анекдот из более чем тысячной базы данных"

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