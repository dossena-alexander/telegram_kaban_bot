from header import bot
from config import PATH
from server.utils.keyboard import InlineKeyboard
from telebot import types


achievements = PATH.HELP+'achievements/'
premium = PATH.HELP+'premium/'
settings = PATH.HELP+'settings/'
user_menu = PATH.HELP+'user_menu/'
commands = PATH.HELP+'commands/'
inline = PATH.HELP+'inline/'


def excursus(call):
    keyboard = InlineKeyboard()
    keyboard.add_button('Достижения', 'USER_EX_ACHIEVEMENTS')
    keyboard.add_button('Премиум', 'USER_EX_PREMIUM')
    keyboard.add_button('Сообщение админу', 'USER_EX_ADMIN_MSG')
    keyboard.add_button('Настройки', 'USER_EX_SETTINGS')
    keyboard.add_button('Команды', 'USER_EX_COMMANDS')
    keyboard.add_button('In-line', 'USER_EX_INLINE')
    photo = open(user_menu+'default.png', 'rb')

    if call.data == "USER_EXCURSUS":
        bot.send_photo(call.message.chat.id, photo, "Помощь по функциям бота", reply_markup=keyboard)
    elif call.data == "USER_EXCURSUS_BACK":
        media = types.InputMediaPhoto(photo)
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    _user_ex_achievements(call)
    _user_ex_premium(call)
    _user_ex_admin_msg(call)
    _user_ex_settings(call)
    _user_ex_commands(call)
    _user_ex_inline(call)


def _user_ex_achievements(call):
    if call.data == "USER_EX_ACHIEVEMENTS":
        photo = open(user_menu+'achievements.png', 'rb') 
        text = '<b>Достижения</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Посмотреть", call="EX_ACHIEVEMENTS_SEE")
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'EX_ACHIEVEMENTS_SEE':
        photo = open(achievements+'achieve_menu.png', 'rb')
        text = "Это меню <b>твоих достижений</b> в Кабане Боте"
        keyboard = InlineKeyboard()
        keyboard.add_button(text='Открытые кабаны', call="EX_ACHIEVEMENTS_BOARS")
        keyboard.add_button(text="Назад", call="USER_EX_ACHIEVEMENTS")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'EX_ACHIEVEMENTS_BOARS':
        photo = open(achievements+'achieve_boars.png', 'rb')
        text = "Это список открытых категорий кабанов"
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_ACHIEVEMENTS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


def _user_ex_premium(call):
    if call.data == "USER_EX_PREMIUM":
        photo = open(user_menu+'premium.png', 'rb') 
        text = '<b>Премиум</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Посмотреть", call="EX_PREMIUM_SEE")
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'EX_PREMIUM_SEE':
        photo = open(premium+'default.png', 'rb')
        text = "Это меню премиума. Здесь ты можешь посмотреть свой статус и сколько дней активен/неактивен твой премиум"
        keyboard = InlineKeyboard()
        keyboard.add_button(text='О премиум', call="EX_PREMIUM_ABOUT")
        keyboard.add_button(text='Отключить премиум', call="EX_PREMIUM_DISABLE")
        keyboard.add_button(text="Назад", call="USER_EX_PREMIUM")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'EX_PREMIUM_ABOUT':
        photo = open(premium+'premium_about.png', 'rb')
        text = "Долгий рассказ зачем тебе нужен премиум..."
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_PREMIUM_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'EX_PREMIUM_DISABLE':
        photo = open(premium+'premium_disable.png', 'rb')
        text = "Кнопка, с помощью которой ты можешь принудительно отключить премиум"
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_PREMIUM_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


def _user_ex_admin_msg(call):
    if call.data == "USER_EX_ADMIN_MSG":
        photo = open(user_menu+'admin_msg.png', 'rb') 
        text = '<b>Сообщение админу</b>\nНажав на кнопку, ты можешь отправить админу сообщение.\nСообщение может быть как просто текстом, картинкой, так и картинкой с подписью (Именно с подписью, а не картинка, а потом текст)'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


def _user_ex_settings(call):
    if call.data == "USER_EX_SETTINGS":
        photo = open(user_menu+'settings.png', 'rb') 
        text = '<b>Настройки</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Посмотреть", call="EX_SETTINGS_SEE")
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_SETTINGS_SEE":
        photo = open(settings+'default.png', 'rb') 
        text = '<b>Доступные настройки</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Уведомления", call="EX_SETTINGS_NOTIFY")
        keyboard.add_button(text="Назад", call="USER_EX_SETTINGS")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_SETTINGS_NOTIFY":
        photo = open(settings+'notify_on.png', 'rb') 
        text = 'Настройка позволяющая включать или отключать уведомления от бота. По умолчанию, включена\nЧто подразумевается под уведомлением?\n1) Сообщение от админа\n2) Сообщение от бота\n3) Сообщение об открытии нового кабана\n4) Сообщение о новом достижении'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Отключение", call="EX_SETTINGS_NOTIFY_OFF")
        keyboard.add_button(text="Назад", call="USER_EX_SETTINGS")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_SETTINGS_NOTIFY_OFF":
        photo = open(settings+'notify_off.png', 'rb') 
        text = 'Чтобы выключить уведомления, достаточно нажать на кнопку. Если на кнопке отобразится ❌ (крестик), то значит, что уведомления отключены, то же и наоборот'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_SETTINGS_NOTIFY")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


def _user_ex_commands(call):
    if call.data == "USER_EX_COMMANDS":
        photo = open(commands+'default.jpg', 'rb') 
        text = '<b>Команды Кабана Бота</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Посмотреть", call="EX_COMMANDS_SEE")
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_SEE":
        photo = open(commands+'commands.jpg', 'rb') 
        text = '<b>Доступные команды</b>'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="/WCT", call="EX_COMMANDS_WCT")
        keyboard.add_button(text="/PHOTO", call="EX_COMMANDS_PHOTO")
        keyboard.add_button(text="/JOKE", call="EX_COMMANDS_JOKE")
        keyboard.add_button(text="/AUTH", call="EX_COMMANDS_AUTH")
        keyboard.add_button(text="/HELP", call="EX_COMMANDS_HELP")
        keyboard.add_button(text="/BOARS", call="EX_COMMANDS_BOARS")
        keyboard.add_button(text="Назад", call="USER_EX_COMMANDS")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_WCT":
        photo = open(commands+'wct.jpg', 'rb') 
        text = '<b>Команда</b> /wct\nСамая главная в Кабане Боте -- позволяет посмотреть какой ты кабан сегодня.\nКабаны выпадают пользователям рандомно. Один кабан на весь день. Кабанов можно собирать и коллекционировать, открывая редкие виды'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_PHOTO":
        photo = open(commands+'photo.jpg', 'rb') 
        text = '<b>Команда</b> /photo\nОтправляет пользователю случайную картинку из бота. Картинки можно предложить админу на рассмотрение, в случае одобрения, картинка будет использоваться в боте'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_JOKE":
        photo = open(commands+'joke.jpg', 'rb') 
        text = '<b>Команда</b> /joke\nОтправляет пользователю случайный анекдот из бота. Анекдоты можно предложить админу на рассмотрение, в случае одобрения, анекдот будет использоваться в боте'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_AUTH":
        photo = open(commands+'auth.jpg', 'rb') 
        text = '<b>Команда</b> /auth\nПозволяет войти в меню пользователя.\nДоступна только в чате с ботом'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Про меню", call="USER_EXCURSUS")
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_HELP":
        photo = open(commands+'help.jpg', 'rb') 
        text = '<b>Команда</b> /help\nТа самая команда, с помощью которой ты это читаешь :)'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_COMMANDS_BOARS":
        photo = open(commands+'boars.jpg', 'rb') 
        text = '<b>Команда</b> /boars\nДоступна в любом чате.\nБот скидывет статистику открытия кабанов'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="В меню пользователя...", call="USER_EX_ACHIEVEMENTS")
        keyboard.add_button(text="Назад", call="EX_COMMANDS_SEE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

def _user_ex_inline(call):
    if call.data == "USER_EX_INLINE":
        photo = open(inline+'default.png', 'rb') 
        text = 'In-line режим бота'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Посмотреть", call="EX_INLINE_SEE")
        keyboard.add_button(text="Назад", call="USER_EXCURSUS_BACK")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_INLINE_SEE":
        photo = open(inline+'step_one.png', 'rb') 
        text = 'Существуют <b>два</b> режима работы in-line'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Фото", call="EX_INLINE_PHOTO")
        keyboard.add_button(text="Анекдот", call="EX_INLINE_JOKE")
        keyboard.add_button(text="Назад", call="USER_EX_INLINE")
        media = types.InputMediaPhoto(photo, text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_INLINE_PHOTO":
        animation = open(inline+'photo.gif', 'rb') 
        text = '<b>Режим фото</b>\nНеобходимо в любом чате упомянуть бота и через пробел написать "фото". Тогда Кабан Бот предложит рандомные фотографии, остается только выбрать, нажав на нужную фотокарточку'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_INLINE_SEE")
        media = types.InputMediaAnimation(media=animation, caption=text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == "EX_INLINE_JOKE":
        animation = open(inline+'jokes.gif', 'rb') 
        text = '<b>Режим анекдот</b>\nНеобходимо в любом чате упомянуть бота и через пробел написать "анекдот". Тогда Кабан Бот предложит рандомные анекдоты, остается только выбрать, нажав на нужный'
        keyboard = InlineKeyboard()
        keyboard.add_button(text="Назад", call="EX_INLINE_SEE")
        media = types.InputMediaAnimation(media=animation, caption=text, parse_mode='html')
        bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
