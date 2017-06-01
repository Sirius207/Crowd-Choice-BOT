
# ========================================================
# Get Info From Telegram Message
# ========================================================

def get_text(update):
    '''get message text or reply data from telegram'''
    if hasattr(update.callback_query, 'data'):
        text = update.callback_query.data
    elif hasattr(update.edited_message, 'text'):
        text = update.edited_message.text
    else:
        text = update.message.text
    return text


def get_first_name(update):
    '''get user first_name from telegram'''
    if hasattr(update.message, 'chat'):
        first_name = update.message.chat.first_name
    elif hasattr(update.edited_message, 'chat'):
        first_name = update.edited_message.chat.first_name
    else:
        first_name = update.callback_query.message.chat.first_name
    return first_name


def get_chat_id(update):
    '''get chat_id from telegram'''
    if hasattr(update.message, 'chat'):
        chat_id = update.message.chat.id
    elif hasattr(update.edited_message, 'chat'):
        chat_id = update.edited_message.chat.id
    else:
        chat_id = update.callback_query.message.chat.id
    return chat_id
