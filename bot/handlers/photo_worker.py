from user.user_funcs import upload_photo


def upload_photo_in_private_chat(message): 
    if message.chat.type == 'private':
        upload_photo(message)