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
        bot.edit_message_text(text=user_translate_menu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    _user_escape(call)

    _user_premium_menu(call)

    _user_achievements(call)

    _user_upload_menu(call)

    _user_about_limits(call)

    _user_settings(call)

    _user_donate_to_admin(call)


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
        bot.edit_message_text(text=premiumMenu.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")
    elif call.data == "ABOUT_PREMIUM":
        text = premium.PremiumMenu.get_text_about()
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="PREMIUM")
        bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")
    elif call.data == "DIS_PREMIUM":
        if userDB.is_premium(call.message.chat.id):
            boarDB = utils.BoarDB()
            userDB.disactivate_premium(call.message.chat.id)
            funcs.new_wct(call.message.chat.id, boarDB)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="PREMIUM")
        bot.edit_message_text(text="<b>Премиум отключен</b>", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")

def _user_upload_menu(call):
    if call.data == "UPLOAD_MENU_USER":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.UPLOAD_MENU_USER)
        bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'UPLOAD_PICTURE':
        bot.edit_message_text(text="Пришли картинку, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, user_funcs.upload_photo)
    elif call.data == 'UPLOAD_JOKE':
        bot.edit_message_text(text="Напиши анекдот, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, user_funcs.upload_joke)


def _user_achievements(call):
    if call.data == "USER_ACHIVE":
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Открытые кабаны", call="ACHIEVEMENTS")
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text='Меню достижений', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")
    elif call.data == "ACHIEVEMENTS":
        achievements = Achievements(call.message.chat.id)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="USER_ACHIVE")
        bot.edit_message_text(text=achievements.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")
    elif call.data == "MEDALS":
        medals = Medals(call.message.chat.id)
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text=medals.get_message(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard, parse_mode="html")


def _user_about_limits(call):
    if call.data == "ABOUT_LIMITS":
        about_limits = (
            '<b>О лимитах</b>\n'
            + 'Лимиты нужны для облегчения работы админа, а также ограничении спама\n'
            + '<i>Лимиты по загрузке:</i>\n'
            + f'<b>Для анекдотов:</b> {LIMIT.JOKE}\n'
            + f'<b>Для фотокарточек:</b> {LIMIT.PHOTO}\n'
            + f'<b>Для сообщений админу:</b> {LIMIT.MESSAGE}\n'
        )
        bot.edit_message_text(text=about_limits, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')


def _user_settings(call):
    if call.data == "USER_SETTINGS":
        keyboard = user_funcs.get_settings_keyboard(call.from_user.id)
        bot.edit_message_text('Настройки', call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "USER_NOTIFY_CANCEL":
        userDB.update_notify_option(call.from_user.id, False)
        keyboard = user_funcs.get_settings_keyboard(call.from_user.id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "USER_NOTIFY_ACCEPT":
        userDB.update_notify_option(call.from_user.id, True)
        keyboard = user_funcs.get_settings_keyboard(call.from_user.id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

def _user_donate_to_admin(call):
    if call.data == "DONATE":
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Админу", call="DONATE_TO_ADMIN")
        keyboard.add_button(text="Дизайнеру", call="DONATE_TO_ADMIN_DESIGNER")
        keyboard.add_button(text="Назад", call="BACK_USER")
        bot.edit_message_text(text='Пожертвование участникам проекта', 
                                 chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 reply_markup=keyboard, parse_mode="html")

    if call.data == "DONATE_TO_ADMIN_DESIGNER":
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="ВТБ", call="USER_DESIGNER_DONATE_VTB")
        keyboard.add_button(text="Тинькофф", call="USER_DESIGNER_DONATE_TINKOFF")
        keyboard.add_button(text="Назад", call="DONATE")
        bot.edit_message_text(text='Донат можно совершить на ВТБ или Тинькофф,' 
                                 + ' по номеру карты', 
                                 chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 reply_markup=keyboard, parse_mode="html")

    elif call.data == 'USER_DESIGNER_DONATE_VTB':
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Номер карты", call="USER_DESIGNER_DONATE_VTB_CARD")
        keyboard.add_button(text="Назад", call="DONATE_TO_ADMIN_DESIGNER")
        bot.edit_message_text('Донат через ВТБ', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == 'USER_DESIGNER_DONATE_VTB_CARD':
        keyboard = utils.InlineKeyboard()
        text = '<code>2200240468876244</code>'
        keyboard.add_button(text="Назад", call="USER_DESIGNER_DONATE_VTB")
        bot.edit_message_text('Донат по номеру карты\nПросто нажми на номер\n\n'+text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    elif call.data == 'USER_DESIGNER_DONATE_TINKOFF':
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Номер карты", call="USER_DESIGNER_DONATE_TINKOFF_CARD")
        keyboard.add_button(text="Назад", call="DONATE_TO_ADMIN_DESIGNER")
        bot.edit_message_text('Донат через Тинькофф', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == 'USER_DESIGNER_DONATE_TINKOFF_CARD':
        keyboard = utils.InlineKeyboard()
        text = '<code>2200700153280754</code>'
        keyboard.add_button(text="Назад", call="USER_DESIGNER_DONATE_TINKOFF")
        bot.edit_message_text('Донат по номеру карты\nПросто нажми на номер\n\n'+text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    if call.data == "DONATE_TO_ADMIN":
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Сбер", call="USER_ADMIN_DONATE_SBER")
        keyboard.add_button(text="Тинькофф", call="USER_ADMIN_DONATE_TINKOFF")
        keyboard.add_button(text="Назад", call="DONATE")
        bot.edit_message_text(text='Донат админу можно совершить на Сбер или Тинькофф,' 
                                 + ' по номеру карты или с помощью удобных сервисов', 
                                 chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 reply_markup=keyboard, parse_mode="html")

    elif call.data == 'USER_ADMIN_DONATE_SBER':
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="Сбер чаевые", call="USER_ADMIN_DONATE_SBER_DONATE")
        keyboard.add_button(text="Номер карты", call="USER_ADMIN_DONATE_SBER_CARD")
        keyboard.add_button(text="Назад", call="DONATE_TO_ADMIN")
        bot.edit_message_text('Донат через сбер', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == 'USER_ADMIN_DONATE_SBER_CARD':
        keyboard = utils.InlineKeyboard()
        text = '<code>5469350013277563</code>'
        keyboard.add_button(text="Назад", call="USER_ADMIN_DONATE_SBER")
        bot.edit_message_text('Донат по номеру карты\nПросто нажми на номер\n\n'+text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    elif call.data == 'USER_ADMIN_DONATE_SBER_DONATE':
        keyboard = utils.InlineKeyboard()
        link = 'https://pay.mysbertips.ru/82608561'
        keyboard.add_button(text="Назад", call="USER_ADMIN_DONATE_SBER")
        bot.edit_message_text('Донат через Сбер чаевые\n'+link, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    elif call.data == 'USER_ADMIN_DONATE_TINKOFF':
        keyboard = utils.InlineKeyboard()
        keyboard.add_button(text="CloudTips", call="USER_ADMIN_DONATE_TINKOFF_DONATE")
        keyboard.add_button(text="Номер карты", call="USER_ADMIN_DONATE_TINKOFF_CARD")
        keyboard.add_button(text="Тинькофф сбор", call="USER_ADMIN_DONATE_TINKOFF_COLLECTING")
        keyboard.add_button(text="Назад", call="DONATE_TO_ADMIN")
        bot.edit_message_text('Донат через сбер', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == 'USER_ADMIN_DONATE_TINKOFF_CARD':
        keyboard = utils.InlineKeyboard()
        text = '<code>5469350013277563</code>'
        keyboard.add_button(text="Назад", call="USER_ADMIN_DONATE_TINKOFF")
        bot.edit_message_text('Донат по номеру карты\nПросто нажми на номер\n\n'+text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    elif call.data == 'USER_ADMIN_DONATE_TINKOFF_COLLECTING':
        keyboard = utils.InlineKeyboard()
        text = 'https://www.tinkoff.ru/cf/6IjR9049vWy'
        keyboard.add_button(text="Назад", call="USER_ADMIN_DONATE_TINKOFF")
        bot.edit_message_text('Донат через Тинькофф сбор\n'+text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')

    elif call.data == 'USER_ADMIN_DONATE_TINKOFF_DONATE':
        keyboard = utils.InlineKeyboard()
        link = 'https://pay.cloudtips.ru/p/b256f4c7'
        keyboard.add_button(text="Назад", call="USER_ADMIN_DONATE_TINKOFF")
        bot.edit_message_text('Донат через Тинькофф CloudTips\n'+link, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='html')
