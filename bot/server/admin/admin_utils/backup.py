import shutil
from time import sleep
from datetime import datetime
from config import PATH, ADMIN_ID, SERVICE_CHANNEL
from server.utils.charts.collector import Time


def admin_backup():
    current_date = datetime.now(Time.msc_tz).date()
    current_time = Time(now=True).time
    stats_path = PATH.DB_STATS
    main_path = PATH.MAIN_DB
    main_zip_name = shutil.make_archive(PATH.BACKUP+'main/'+f'main ({current_date}--{current_time})', 'zip', main_path)
    stats_zip_name = shutil.make_archive(PATH.BACKUP+'stats/'+f'stats ({current_date}--{current_time})', 'zip', stats_path)
    return main_zip_name, stats_zip_name, current_date, current_time


def admin_backup_dir(to: str, zipname: str, path: str):
    """Archive any dir

    Args:
        to (str): path to save zip
        zipname (str): zip name + date and time
        path (str): dir to zip

    Returns:
        str: path to zip
        date: date saving zip
        str: time saving zip
    """
    current_date = datetime.now(Time.msc_tz).date()
    current_time = Time(now=True).time
    zip_name = shutil.make_archive(to+f'{zipname}'+f'({current_date}--{current_time})', 'zip', path)
    return zip_name, current_date, current_time


def c_backup(bot):
    while True:
        time = Time(now=True)
        if time.hour == 12:
            current_time = time.time
            current_date = datetime.now(Time.msc_tz).date()
            stats_path = PATH.DB_STATS
            main_path = PATH.MAIN_DB
            main_zip_name = shutil.make_archive(PATH.BACKUP+'main/'+f'main ({current_date}--{current_time})', 'zip', main_path)
            stats_zip_name = shutil.make_archive(PATH.BACKUP+'stats/'+f'stats ({current_date}--{current_time})', 'zip', stats_path)
            bot.send_document(SERVICE_CHANNEL, open(main_zip_name, 'rb'), caption=f'Бекап MAIN\n<b>{current_date}</b> <b>({time})</b>\n#backup', parse_mode='html')
            bot.send_document(SERVICE_CHANNEL, open(stats_zip_name, 'rb'), caption=f'Бекап STATS\n<b>{current_date}</b> <b>({time})</b>\n#backup', parse_mode='html')
            bot.send_message(ADMIN_ID, 'Бэкап создан (на сервере) и отослан в сервисный канал')
        sleep(60*60*15)
