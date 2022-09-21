import random
from telebot import types
from server.handlers.inline.ImageParser import YandexImage
from header import adminPicDB, adminJokeDB, bot


def query_text(query):
    offset = int(query.offset) if query.offset else 5
    if query.query.lower() == 'анекдот':
        results = create_jokes(offset)
        bot.answer_inline_query(query.id, results, next_offset=str(offset + 5), cache_time=30)
    if query.query.lower() == 'фото':
        results = create_photos(offset)
        bot.answer_inline_query(query.id, results, next_offset=str(offset + 5), cache_time=60)
    elif query.query.lower().split()[0] == 'фото' and query.query.lower().split()[1]: # The first word in query 'фото котик'
        results = create_yandex_photos(query.query.lower().split()[1:], offset)
        bot.answer_inline_query(query.id, results, next_offset=str(offset + 5), cache_time=30)


def empty_query(query):
    r = types.InlineQueryResultArticle(
            id='1',
            title="Кабан бот",
            description="Напиши \"анекдот\" или \"фото\"",
            input_message_content=types.InputTextMessageContent(
            message_text="Кабан бот - Пришли друзьям смешнявку)")
    )
    bot.answer_inline_query(query.id, [r])


def create_jokes(offset: int):
    def get_joke() -> list[str]:
        return adminJokeDB.get_record(row=random.randint(0, adminJokeDB.get_records_count() - 1)) 

    jokes = [get_joke() for _ in range(offset + 1)]
    return [types.InlineQueryResultArticle(
                id=str(c), title="Анекдот",
                description=v,
                input_message_content=types.InputTextMessageContent(
                message_text=v)
            ) for c, v in enumerate(jokes)]


def create_photos(offset: int):
    def get_photo() -> list[str]:
        return adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1), col=1)

    photos = [get_photo() for _ in range(offset + 1)]
    return [types.InlineQueryResultCachedPhoto(id = str(c), photo_file_id=v) 
                                                    for c, v in enumerate(photos)]


def create_yandex_photos(query: str, offset: int) -> list[types.InlineQueryResultPhoto]:
    parser = YandexImage()
    results = (item for item in parser.gen_search(query))
    def photos():
        i = 0
        for item in results:
            if item != '':
                yield i, item.url, item.preview.url
                i += 1

    return [types.InlineQueryResultPhoto(id=str(c), photo_url=url, thumb_url=thumb) 
                                            for c, url, thumb in photos()]

