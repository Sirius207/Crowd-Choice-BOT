
import hashlib

from config import bot_config
HASHKEY = bot_config['HASHKEY']

def check_hash(chat_id, hash_value):
    '''check hash value is valid'''
    check_hash_value = hashlib.sha224(str(chat_id + HASHKEY)).hexdigest()
    return check_hash_value == hash_value
