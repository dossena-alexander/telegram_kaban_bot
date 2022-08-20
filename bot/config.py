API_TOKEN = ""
ADMIN_ID = 0
WCT_CHANNEL = 0
PHOTO_CHANNEL = 0
JOKE_CHANNEL = 0
#========================MSG======================================

class BOT_MESSAGE():
    USER = "Меню пользователя"
    ADMIN = "Админ меню"
    USER_SUB_MENU = "Кабаний перевод телеграмм для настоящих кабанов, просто нажми на кнопку, чтобы установить"
    def HELP(photo_count: int = 1000, joke_count: int = 1000) -> str:
        msg = ("<b>Что я умею</b>\n <i>Мои команды:</i>\n"
            + "• /auth - Аутентификация\n" 
            + "• /help - Помощь\n"
            + "• /keys - Клавиатура\n"
            + "• /hide - Спрятать клавиатуру\n"
            + "<i>Мои возможности:</i>\n" 
            + "• <b>Какой ты кабан сегодня</b>\n"
            + f"• <b>Фотокарточка</b> –– Смешная картинка из {photo_count}\n"
            + f"• <b>Анекдот</b> –– Рандомный анекдот из {joke_count}")
        return msg

#========================KEYS=====================================

class KEYS():
    ADMIN = {
        0: { "text": "Предложения",               "call": "SUGGESTIONS"       }, 
        1: { "text": "Загрузка",                  "call": "UPLOAD_MENU_ADMIN" },
        2: { "text": "Сообщения",                 "call": "SEE_MESSAGES"      }, 
        3: { "text": "Рассылка",                  "call": "NOTIFY_MENU"       },
        4: { "text": "Остановить бота",           "call": "STOP_BOT"          },
        5: { "text": "Пользователь",              "call": "USER"              }, 
        6: { "text": "Статистика",                "call": "STATISTICS"        },
    }
    USER = {
        0: { "text": "Загрузить",                 "call": "UPLOAD_MENU_USER"  }, 
        1: { "text": "Сообщение админу",          "call": "MESSAGE_TO_ADMIN"  },
        2: { "text": "Достижения",                "call": "ACHIEVEMENTS"      }, 
        3: { "text": "Премиум",                   "call": "PREMIUM"           },
        4: { "text": "Кабаний перевод телеграмм", "call": "TRANSLATE"         },  
    }
    START = {
        0: { "text": "Анекдот",                   "call": "None"              }, 
        1: { "text": "Фотокарточка",              "call": "None"              },
        2: { "text": "Какой я кабан сегодня",     "call": "None"              }, 
    }
    NOTIFY = {
        0: { "text": "Как админ",                 "call": "NOTIFY"            }, 
        1: { "text": "Как бот",                   "call": "NOTIFY_BOT"        },
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
        0: { "text": "❌",                   "call": "JOKE_DELETE"       }, 
        1: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        2: { "text": "✅",                   "call": "JOKE_ACCEPT"       }, 
        3: { "text": "◀",                         "call": "JOKE_PREV"         },
        4: { "text": "0/0",                       "call": "COUNTER"           },
        5: { "text": "▶",                         "call": "JOKE_FURTHER"      },
    }
    PIC_SEE = {
        0: { "text": "❌",                   "call": "PIC_DELETE"        }, 
        1: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        2: { "text": "✅",                   "call": "PIC_ACCEPT"        }, 
        3: { "text": "◀",                         "call": "PIC_PREV"          },
        4: { "text": "0/0",                       "call": "COUNTER"           },
        5: { "text": "▶",                         "call": "PIC_FURTHER"       },
    }
    MSG_SEE = {
        0: { "text": "Выйти",                     "call": "BACK_ADMIN"        }, 
        1: { "text": "❌",                   "call": "MSG_DELETE"        }, 
        2: { "text": "◀",                         "call": "MSG_PREV"          },
        3: { "text": "0/0",                       "call": "COUNTER"           },
        4: { "text": "▶",                         "call": "MSG_FURTHER"       },
    }
    SUGGESTIONS = {
        0: { "text": "Картинки",                  "call": "SEE_PICTURES"      }, 
        1: { "text": "Анекдоты",                  "call": "SEE_JOKES"         },
        2: { "text": "Назад",                     "call": "BACK_ADMIN"        }, 
    }
    CATEGORY = {
        0: { "text": "emotions",                  "call": "1"                  }, 
        1: { "text": "interesting",               "call": "2"                  },
        2: { "text": "game",                      "call": "3"                  }, 
        3: { "text": "world",                     "call": "4"                  }, 
        4: { "text": "trap",                      "call": "5"                  },
        5: { "text": "big",                       "call": "6"                  }, 
        6: { "text": "small",                     "call": "7"                  }, 
        7: { "text": "phylosophy",                "call": "8"                  },
        8: { "text": "upper_stratum",             "call": "9"                  }, 
        9: { "text": "sub_culture",               "call": "10"                 }, 
    }
    

#========================LIMITS===================================

# limits for user per day
class LIMIT():
    JOKE = 10
    MESSAGE = 5
    PHOTO = 10


class PREMIUM_LIMIT():
    UPLOADS_COUNT = 5
    DAYS = 2

UPLOAD_LOCK = False

#========================FILTER===================================

# text-worker filter
class FILTER():
    COMMANDS = [
            "Фотокарточка", 
            "Анекдот", 
            "Какой я кабан сегодня", 
            "/auth", "/help", "/start",
            "/hide", "/keys"
    ]

#========================PATHS====================================

# path to folders
class PATH():
    WCT = '../materials/wct/'
    PHOTOS = '../materials/photos/'
    RECIEVED_PHOTOS = '../materials/recieved_photos/'
    DB = '../db/main.db'
    LOG = "../Logs/bot.log"
