import shutil
from datetime import date
from config import PATH, ADMIN_ID, SERVICE_CHANNEL
from server.utils.charts.collector import Time


def admin_backup():
    current_date = date.today()
    current_time = Time(now=True).time
    stats_path = PATH.DB_STATS
    main_path = PATH.MAIN_DB
    main_zip_name = shutil.make_archive(PATH.BACKUP+f'main ({current_date}--{current_time})', 'zip', main_path)
    stats_zip_name = shutil.make_archive(PATH.BACKUP+f'stats ({current_date}--{current_time})', 'zip', stats_path)
    return main_zip_name, stats_zip_name, current_date, current_time


def c_backup(bot):
    while True:
        time = Time(now=True)
        if time.hour == 12 or time.hour == 21:
            current_time = time.time
            current_date = date.today()
            stats_path = PATH.DB_STATS
            main_path = PATH.MAIN_DB
            main_zip_name = shutil.make_archive(PATH.BACKUP+f'main ({current_date}--{current_time})', 'zip', main_path)
            stats_zip_name = shutil.make_archive(PATH.BACKUP+f'stats ({current_date}--{current_time})', 'zip', stats_path)
            bot.send_document(SERVICE_CHANNEL, open(main_zip_name, 'rb'), caption=f'Бекап MAIN\n<b>{date}</b> <b>({time})</b>\n#backup', parse_mode='html')
            bot.send_document(SERVICE_CHANNEL, open(stats_zip_name, 'rb'), caption=f'Бекап STATS\n<b>{date}</b> <b>({time})</b>\nbackup', parse_mode='html')
            bot.send_message(ADMIN_ID, 'Бэкап создан (на сервере) и отослан в сервисный канал')
