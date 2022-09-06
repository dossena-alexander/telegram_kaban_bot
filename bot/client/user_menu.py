from header import bot, userMenu, user_translate_menu
from header import utils
from config import KEYS, LIMIT

from server.user.user_utils import *
from server.user.user_utils import premium
import server.user.user_funcs as user_funcs


def user_menu(call):

    if call.data == "MESSAGE_TO_ADMIN":
        bot.edit_message_text(text="Напиши сообщение или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Отправить можно только текст или картинку (необязательно с подписью)")
        bot.register_next_step_handler(call.message, user_funcs.upload_message_to_admin)

    elif call.data == "TRANSLATE":
        keyboard = utils.InlineKeyboard()
        keyboard.add_url_button("Русский", "https://t.me/setlanguage/ru")
        keyboard.add_url_button("Кабаний", "https://t.me/setlanguage/kabanchikoff")
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=user_translate_menu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    
    _user_escape(call)

    _user_premium_menu(call)

    _user_achievements(call)

    _user_upload_menu(call)

    _user_about_limits(call)

    _donate_to_admin(call)


def _user_escape(call):
    if call.data == "BACK_USER":
        bot.edit_message_text(text=userMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.get_inline_keyboard())


def _user_premium_menu(call):
    if call.data == "PREMIUM":
        premiumMenu = premium.PremiumMenu(call.message.chat.id)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="О премиум", call="ABOUT_PREMIUM")
        keyboard.add_button(text="Отключить премиум", call="DIS_PREMIUM")
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=premiumMenu.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")
    elif call.data == "ABOUT_PREMIUM":
        text = premium.PremiumMenu.get_text_about()
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")
    elif call.data == "DIS_PREMIUM":
        if userDB.is_premium(call.message.chat.id):
            boarDB = utils.BoarDB()
            userDB.disactivate_premium(call.message.chat.id)
            funcs.new_wct(call.message.chat.id, boarDB)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text="<b>Премиум отключен</b>", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")

def _user_upload_menu(call):
    if call.data == "UPLOAD_MENU_USER":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.UPLOAD_MENU_USER)
        bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get())
    elif call.data == 'UPLOAD_PICTURE':
        bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, user_funcs.upload_photo)
    elif call.data == 'UPLOAD_JOKE':
        bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, user_funcs.upload_joke)


def _user_achievements(call):
    if call.data == "ACHIEVEMENTS":
        achievements = Achievements(call.message.chat.id)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=achievements.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")
    elif call.data == "MEDALS":
        medals = Medals(call.message.chat.id)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=medals.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.get(), parse_mode="html")


def _user_about_limits(call):
    if call.data == "ABOUT_LIMITS":
        about_limits = (
            '<b>О лимитах</b>\n'
            + 'Лимиты нужны для облегчения работы админа, а также ограничении спама'
            + '<i>Лимиты по загрузке:</i>\n'
            + f'<b>Для анекдотов:</b> {LIMIT.JOKE}'
            + f'<b>Для фотокарточек:</b> {LIMIT.PHOTO}'
            + f'<b>Для сообщений админу:</b> {LIMIT.MESSAGE}'
        )
        bot.edit_message_text(text=about_limits, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')


def _donate_to_admin(call):
    if call.data == "DONATE_TO_ADMIN":
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text='Донат админу', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")