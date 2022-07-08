API_TOKEN = ""
ADMIN_ID = 0
#========================MSG======================================

class BOT_MESSAGE():
    USER = "Меню пользователя"
    ADMIN = "Админ меню"
    USER_SUB_MENU = "Кабаний перевод телеграмм для настоящих кабанов, просто нажми на кнопку, чтобы установить"
    def HELP(photo_count: int = 1000, joke_count: int = 1000) -> str:
        msg = f"<b>Что я умею</b>\n <i>Мои команды:</i>\n • /start - Запуск\n • /help - Помощь\n • /auth - Аутентификация\n <i>Мои возможности:</i>\n • <b>Какой ты кабан сегодня</b>\n • <b>Фотокарточка</b> –– Смешная картинка из {photo_count}\n • <b>Анекдот</b> –– Рандомный анекдот из {joke_count}"
        return msg

#========================KEYS=====================================

class KEYS():
    ADMIN = {
        0: { "text": "Предложения",               "call": "SUGGESTIONS"       }, 
        1: { "text": "Загрузка",                  "call": "UPLOAD_MENU_ADMIN" },
        2: { "text": "Сообщения",                 "call": "SEE_MESSAGES"      }, 
        3: { "text": "Рассылка",                  "call": "NOTIFY"            },
        4: { "text": "Остановить бота",           "call": "STOP_BOT"          },
        5: { "text": "Пользователь",              "call": "USER"              }, 
        6: { "text": "Статистика",                "call": "STATISTICS"        },
    }
    USER = {
        0: { "text": "Загрузить",                 "call": "UPLOAD_MENU_USER"  }, 
        1: { "text": "Сообщение админу",          "call": "MESSAGE_TO_ADMIN"  },
        2: { "text": "Кабаний перевод телеграмм", "call": "TRANSLATE"         }, 
    }
    START = {
        0: { "text": "Анекдот",                   "call": "None"              }, 
        1: { "text": "Фотокарточка",              "call": "None"              },
        2: { "text": "Какой я кабан сегодня",     "call": "None"              }, 
    }
    USER_SUB_MENU = {
        0: { "text": "Русский",                   "call": "None"              }, 
        1: { "text": "Кабаний",                   "call": "None"              },
        2: { "text": "Назад",                     "call": "BACK_USER"         }, 
    }
    UPLOAD_MENU_USER = {
        0: { "text": "Картинку",                  "call": "UPLOAD_PICTURE"    }, 
        1: { "text": "Анекдот",                   "call": "UPLOAD_JOKE"       },
        2: { "text": "Назад",                     "call": "BACK_USER"         }, 
    }
    UPLOAD_MENU_ADMIN = {
        0: { "text": "Картинку",                  "call": "UPLOAD_PICTURE"    }, 
        1: { "text": "Анекдот",                   "call": "UPLOAD_JOKE"       },
        2: { "text": "Кабана",                    "call": "UPLOAD_BOAR"       }, 
        3: { "text": "Премиум Кабана",            "call": "UPLOAD_PREM_BOAR"  }, 
    }
    JOKE_SEE = {
        0: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        1: { "text": "Далее",                     "call": "JOKE_FURTHER"      },
        2: { "text": "Принять",                   "call": "JOKE_ACCEPT"       }, 
        3: { "text": "Удалить",                   "call": "JOKE_DELETE"       }, 
    }
    PIC_SEE = {
        0: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        1: { "text": "Далее",                     "call": "PIC_FURTHER"       },
        2: { "text": "Принять",                   "call": "PIC_ACCEPT"        }, 
        3: { "text": "Удалить",                   "call": "PIC_DELETE"        }, 
    }
    MSG_SEE = {
        0: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        1: { "text": "Далее",                     "call": "MSG_FURTHER"       },
        2: { "text": "Удалить",                   "call": "MSG_DELETE"        }, 
    }
    SUGGESTIONS = {
        0: { "text": "Картинки",                  "call": "SEE_PICTURES"      }, 
        1: { "text": "Анекдоты",                  "call": "SEE_JOKES"         },
        2: { "text": "Назад",                     "call": "BACK_ADMIN"        }, 
    }

#========================LIMITS===================================

# limits for user per day
class LIMIT():
    JOKE = 10
    MESSAGE = 5
    PHOTO = 10


class UPLOAD_LIMIT():
    COUNT = 5

#========================FILTER===================================

# text-worker filter
class FILTER():
    COMMANDS = [
            "Фотокарточка", 
            "Анекдот", 
            "Какой я кабан сегодня", 
            "Расписание"
            "/auth", "/help", "/start"
]

#========================PATHS====================================

# path to folders
class PATH():
    WCT = '../wct/'
    PHOTOS = '../photos/'
    RECIEVED_PHOTOS = '../recieved_photos/'
    DB = '../db/main.db'
    LOG = "../Logs/bot.log"
    SHEDULE = "../Shedule/"

#=================================================================

SHEDULE_SITE = ""