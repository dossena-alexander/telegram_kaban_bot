from telebot import types
from header import adminPicDB, random, adminJokeDB, bot


def query_text(query):
    offset = int(query.offset) if query.offset else 5
    if query.query.lower() == 'анекдот':
        results = create_jokes(offset)
        bot.answer_inline_query(query.id, results, next_offset=str(offset + 5))
    # elif query.query.lower() == 'фотокарточка':
    #     results = create_photos(offset)
    #     bot.answer_inline_query(query.id, results, next_offset=str(offset + 5))


def empty_query(query):
    try:
        r = types.InlineQueryResultArticle(
                id='1',
                title="Кабан бот",
                description="Пришли друзьям анекдот)",
                input_message_content=types.InputTextMessageContent(
                message_text="Кабан бот - Пришли друзьям анекдот)")
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)


def create_jokes(offset):
    size = offset
    i = 0
    jokes = []
    while i <= size:
        jokes.append( adminJokeDB.get_record(row=random.randint(0, adminJokeDB.get_records_count() - 1)) )
        i += 1
    i = 0
    results = [types.InlineQueryResultArticle(
        id=str(i), title="Анекдот",
        description=jokes[i],
        input_message_content=types.InputTextMessageContent(
        message_text=jokes[i])
    ) for i in range(len(jokes))]
    return results


# def create_photos(offset):
#     size = offset
#     i = 0
#     photos = []
#     while i <= size:
#         photos.append( adminPicDB.get_record(row=random.randint(0, adminPicDB.get_records_count() - 1)) )
#         photos[i] = 'photos/' + photos[i][:-4]
#         i += 1
#     print(photos)
#     i = 0
#     results = [types.InlineQueryResultCachedPhoto(
#         id = str(i),
#         photo_file_id=photos[i]
#     ) for i in range(len(photos))]

#     return results