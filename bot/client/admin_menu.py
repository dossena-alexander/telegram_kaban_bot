from datetime import date
import shutil, os, time
from header import adminMenu, userMenu
from header import userPicDB, adminPicDB, adminJokeDB, userJokeDB
from config import KEYS, PHOTO_CHANNEL, JOKE_CHANNEL, SERVICE_CHANNEL
from server import utils
from server.utils.charts.charts_menu import get_charts_keyboard, translate_b_call, reverse_b_call
import server.admin.admin_utils as admin_utils
from server.admin.admin_utils.statistics import Statistics, ImageStatistic
from server.utils.charts.chart import Chart
from server.utils.charts.collector import DayStatClickCollector, DateStatClickCollector
from server.admin.admin_funcs import *
from server.utils.charts.collector import Time


suggestions = admin_utils.Suggestions()


def admin_menu(call):
    if call.data == "STATISTICS":
        current_date = date.today()
        current_time = Time(now=True).time
        stats = Statistics()
        back = utils.InlineKeyboard()
        back.add_button(text="Количественная", call="IMG_STATISTICS")
        back.add_button(text="Назад", call="BACK_ADMIN")
        bot.edit_message_text(text=stats.get(), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back.get(), parse_mode="html")
        bot.send_message(SERVICE_CHANNEL, f'<b>{current_date} ({current_time})</b>\n'+stats.get()+'\n#actual', parse_mode='html')
        del stats

    elif call.data == "IMG_STATISTICS":
        current_date = date.today()
        current_time = Time(now=True).time
        stats = Statistics()
        img_s = ImageStatistic()
        stats.get_img_stats(img_s)
        photo = img_s.path

        back = utils.InlineKeyboard()
        back.add_button(text="Назад", call="BACK_ADMIN")
        time.sleep(1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_photo(call.message.chat.id, open(photo, 'rb'), caption='Количественная статистика', reply_markup=back)
        bot.send_photo(SERVICE_CHANNEL, open(photo, 'rb'), caption=f'Статистика на\n<b>{current_date} ({current_time})</b>\n#photo_stat', parse_mode='html')
        del stats
        del img_s
    
    elif call.data == "STOP_BOT":
        utils.log.info("ОСТАНОВКА БОТА")
        bot.stop_polling()

    elif call.data == "SUGGESTIONS":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.SUGGESTIONS)
        bot.edit_message_text(text="Предложения", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    elif call.data == "UPLOAD_MENU_ADMIN":
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.UPLOAD_MENU_ADMIN)
        keyboard.add_button(text="Назад", call="BACK_ADMIN")
        bot.edit_message_text(text="Загрузить", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    elif call.data == "USER": 
        bot.edit_message_text(text=userMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=userMenu.get_inline_keyboard())
    
    _admin_escape(call)

    _admin_notify_menu(call)

    _admin_upload_boars_menu(call)

    _admin_see_pictures_suggestions(call)

    _admin_see_jokes_suggestions(call)

    _admin_see_messages_from_users(call)

    _admin_charts(call)

    _admin_ban_user(call)

    _admin_zip(call)

    _admin_see_files(call)


def _admin_escape(call):
    if call.data == "BACK_ADMIN":
        adminMenu.set_message("Админ меню")
        if suggestions.exist():
            adminMenu.set_message(suggestions.get_message())
        try:
            bot.edit_message_text(text=adminMenu.message, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adminMenu.get_inline_keyboard())
        except:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(text=adminMenu.message, chat_id=call.message.chat.id, reply_markup=adminMenu.get_inline_keyboard())
    

def _admin_notify_menu(call):
    if call.data == "NOTIFY_MENU": 
        keyboard = utils.InlineKeyboard()
        keyboard.set(KEYS.NOTIFY)
        keyboard.add_button("Назад", "BACK_ADMIN")
        bot.edit_message_text(text="Рассылка", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    elif call.data == "NOTIFY":
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, admin_notify)

    elif call.data == "NOTIFY_BOT":
        bot.edit_message_text(text="Напиши сообщение пользователям, или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, bot_notify)


def _admin_upload_boars_menu(call):
    if call.data == "UPLOAD_BOAR":
        keyboard = utils.ReplyKeyboard()
        keyboard.set(KEYS.CATEGORY)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(text="Выбери категорию кабана\nДля отмены нажми /brake", chat_id=call.message.chat.id, reply_markup=keyboard)
        bot.register_next_step_handler(call.message, choose_boar_category)

    elif call.data == "UPLOAD_PREM_BOAR":
        bot.edit_message_text(text="Отправь фото или нажми /brake", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, upload_premium_wct)


def _admin_see_pictures_suggestions(call):
    if call.data == "SEE_PICTURES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif "PIC_ACCEPT" in call.data:
        user_id = int(call.data.split()[1])
        photo_name = userPicDB.get_record(mesg.count)
        photo_id = userPicDB.get_record(mesg.count, col=1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        user_name = userPicDB.get_record(mesg.count, 3)
        adminPicDB.insert(photo_name, photo_id, user_id, user_name)
        bot.send_photo(PHOTO_CHANNEL, photo_id)
        bot.send_notification(user_id, 'Ваше предложение (фотокарточка) принято')
        
        userPicDB.delete_record(photo_name)
        shutil.move(PATH.RECIEVED_PHOTOS + photo_name, PATH.PHOTOS)
        
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)

    elif call.data == "PIC_DELETE":    
        bot.delete_message(call.message.chat.id, call.message.message_id)
        os.remove(PATH.RECIEVED_PHOTOS + userPicDB.get_record(mesg.count))
        userPicDB.delete_record(userPicDB.get_record(mesg.count))
        see_suggestions(call.message, type="pic", db=userPicDB, keys=KEYS.PIC_SEE)


def _admin_see_jokes_suggestions(call):
    if call.data == "SEE_JOKES": 
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif "JOKE_ACCEPT" in call.data:
        user_id = int(call.data.split()[1])
        joke = userJokeDB.get_record(mesg.count)
        text = userJokeDB.get_record(mesg.count, 3)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        adminJokeDB.new_record(joke)
        bot.send_message(JOKE_CHANNEL, text)
        bot.send_notification(user_id, 'Ваше предложение (анекдот) принято')

        userJokeDB.delete_record(joke)
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)

    elif call.data == "JOKE_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        userJokeDB.delete_record(userJokeDB.get_record(mesg.count))
        see_suggestions(call.message, "txt", userJokeDB, KEYS.JOKE_SEE)


def _admin_see_messages_from_users(call):
    if call.data == "SEE_MESSAGES":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_FURTHER":
        mesg.count += 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_PREV":
        mesg.count -= 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)

    elif call.data == "MSG_DELETE":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if msgDB.msg_has_file_id(mesg.count):
            os.remove(PATH.RECIEVED_PHOTOS + msgDB.get_file_id(mesg.count))
        msgDB.delete_msg_and_file_id(mesg.count)
        see_messages_to_admin(call.message, KEYS.MSG_SEE)


def _admin_charts(call):
    def charts_menu(call):
        keyboard = utils.InlineKeyboard()
        keys = utils.build_buttons(KEYS.ADMIN_CHARTS)
        keyboard.add(*keys, row_width=1)
        bot.edit_message_text('Выбери график', call.message.chat.id, 
                                call.message.message_id,
                                reply_markup=keyboard)

    if call.data == "CHARTS":
        charts_menu(call)

    elif 'SEE_CHARTS_DAY' in call.data:
        keyboard = get_charts_keyboard(0, '', 'CHARTS_YEAR', 'CHARTS')
        bot.edit_message_text('Доступные года', call.message.chat.id, 
                                call.message.message_id,
                                reply_markup=keyboard)

    elif call.data.split()[0] == '>':
        offset = int(call.data.split()[1])
        try:
            year = call.data.split()[2]
        except:
            year = '/'
        try:
            month = call.data.split()[3]
        except:
            month = '/'
        b_call = call.data.split()[4]
        keyboard = get_charts_keyboard(offset, year+'/'+month+'/', b_call, reverse_b_call(b_call)+' '+year+'/')
        try:
            date = f'{year}/{month}'
            if month == '/':
                date = f'{year}'
            bot.edit_message_text(f'Доступные {translate_b_call(b_call)} ({date})', call.message.chat.id, 
                                    call.message.message_id,
                                    reply_markup=keyboard)
        except:
            pass
        
    elif '<' in call.data:
        offset = int(call.data.split()[1])
        if offset <= 0:
            offset = 0 
        try:
            year = call.data.split()[2]
        except:
            year = '/'
        try:
            month = call.data.split()[3]
        except:
            month = '/'
        b_call = call.data.split()[4]
        keyboard = get_charts_keyboard(offset, year+'/'+month+'/', b_call, reverse_b_call(b_call)+' '+year+'/')
        try:
            date = f'{year}/{month}'
            if month == '/':
                date = f'{year}'
            bot.edit_message_text(f'Доступные {translate_b_call(b_call)} ({date})', call.message.chat.id, 
                                    call.message.message_id,
                                    reply_markup=keyboard)
        except:
            pass


    elif 'CHARTS_YEAR' in call.data:
        year = call.data.split()[1]
        keyboard = get_charts_keyboard(0, year+'/', 'CHARTS_MONTH', 'SEE_CHARTS_DAY')
        bot.edit_message_text(f'Доступные месяцы ({year})', call.message.chat.id, 
                                call.message.message_id,
                                reply_markup=keyboard)

    elif 'CHARTS_MONTH' in call.data:
        month = call.data.split()[1]
        year = call.data.split()[2]
        keyboard = get_charts_keyboard(0, year+'/'+month+'/', 'CHART_DAY_SEE', 'CHARTS_YEAR'+' '+year+'/')
        try:
            bot.edit_message_text(f'Доступные графики ({year}/{month})', call.message.chat.id, 
                                    call.message.message_id,
                                    reply_markup=keyboard)
        except:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f'Доступные графики ({year}/{month})', reply_markup=keyboard)
    
    elif call.data == '|<':
        keyboard = get_charts_keyboard(0)
        try:
            bot.edit_message_text('Доступные графики', call.message.chat.id, 
                                    call.message.message_id,
                                    reply_markup=keyboard)
        except:
            pass


    elif '>|' in call.data:
        offset = int(call.data.split()[1])
        keyboard = get_charts_keyboard(offset)
        try:
            bot.edit_message_text('Доступные графики', call.message.chat.id, 
                                    call.message.message_id,
                                    reply_markup=keyboard)
        except:
            pass

    elif 'CHART_DAY_SEE' in call.data:
        file = call.data.split()[1]
        path = file.split('-')
        year = path[0]
        month = path[1][1:]

        targets = ['joke_clicks', 'wct_clicks', 'photo_clicks']
        collector = DayStatClickCollector(targets, target_file=file)
        chart = Chart(PATH.CHARTS, collector)
        chart.draw()
        chart_photo = chart.fig_name

        photo = open(PATH.CHARTS+chart_photo, 'rb')

        keyboard = utils.InlineKeyboard()
        keyboard.add_button('Назад', f'CHARTS_MONTH {month} {year}')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_photo(call.message.chat.id, photo, reply_markup=keyboard)

    elif call.data == "CHARTS_WEEK":
        back = utils.InlineKeyboard()
        back.add_button('Назад', 'BACK_FROM_CHARTS')
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "CHARTS_MONTH":
        back = utils.InlineKeyboard()
        back.add_button('Назад', 'BACK_FROM_CHARTS')
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "BACK_FROM_CHARTS":
        bot.delete_message(call.message.chat.id, call.message.message_id)


def _admin_ban_user(call):
    def ban(user_id: int):
        try:
            user_name = bot.get_chat_member(user_id, user_id).user.username
            banDB = BannedDB()
            banDB.ban(user_id, user_name)
            del banDB
        except Exception as e:
            return 'Пользователь заблокировал бота или пользователя с таким id нет'
    if 'ADMIN_BAN_USER' in call.data:
        user_id = int(call.data.split()[1])
        err = ban(user_id)
        if err != None:
            bot.send_message(call.message.chat.id, err)
        else:
            bot.send_message(call.message.chat.id, "Забанил пользователя")


def _admin_zip(call):
    if call.data == 'ADMIN_ZIP':
        keyboard = utils.InlineKeyboard()
        keyboard.add_button('Актуальный БД', 'ADMIN_ZIP_DB')
        keyboard.add_button('Архив БД', 'ADMIN_ZIP_BACKUPS')
        keyboard.add_button('Всех фото', 'ADMIN_ZIP_PHOTO')
        keyboard.add_button('Всех кабанов', 'ADMIN_ZIP_BOARS')
        keyboard.add_button('Назад', 'BACK_ADMIN')
        bot.edit_message_text('Выбери тип бэкапа', call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == 'ADMIN_ZIP_DB':
        main_zip_name, stats_zip_name, date, time = admin_utils.admin_backup()
        bot.send_document(SERVICE_CHANNEL, open(main_zip_name, 'rb'), caption=f'Бекап MAIN\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
        bot.send_document(SERVICE_CHANNEL, open(stats_zip_name, 'rb'), caption=f'Бекап STATS\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
        bot.send_message(call.message.chat.id, 'Бэкап создан (на сервере) и отослан в сервисный канал')

    elif call.data == 'ADMIN_ZIP_BACKUPS':
        zip_name, date, time = admin_utils.admin_backup_dir(PATH.MATERIALS, 'backup_all', PATH.BACKUP)
        bot.send_document(SERVICE_CHANNEL, open(zip_name, 'rb'), caption=f'Бекап архивов БД\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
        bot.send_message(call.message.chat.id, 'Бэкап архива создан и отослан в сервисный канал')
        os.remove(zip_name)

    elif call.data == 'ADMIN_ZIP_PHOTO':
        zip_name, date, time = admin_utils.admin_backup_dir(PATH.MATERIALS, 'backup_photo', PATH.PHOTOS)
        bot.send_document(SERVICE_CHANNEL, open(zip_name, 'rb'), caption=f'Бекап фото\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
        bot.send_message(call.message.chat.id, 'Бэкап фото создан и отослан в сервисный канал')
        os.remove(zip_name)

    elif call.data == 'ADMIN_ZIP_BOARS':
        zip_name, date, time = admin_utils.admin_backup_dir(PATH.MATERIALS, 'backup_wct', PATH.WCT)
        bot.send_document(SERVICE_CHANNEL, open(zip_name, 'rb'), caption=f'Бекап кабанов\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
        bot.send_message(call.message.chat.id, 'Бэкап кабанов создан и отослан в сервисный канал')   
        os.remove(zip_name)
        

def _admin_see_files(call):
    pass