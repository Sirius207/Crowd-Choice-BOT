#!/usr/bin/python
# coding:utf-8

from config import bot_config

redisDB = bot_config['redisDB']

CHAT = 'chat_count'

#
# send chat message
#

def get_chat_count(chat_id):
    ''' get chat_count '''
    chat_count = redisDB.hget(name=chat_id, key=CHAT)
    return chat_count

def plus_chat_count(chat_id):
    '''plus chat count count'''
    chat_count = get_chat_count(chat_id)
    chat_count = int(chat_count) + 1 if chat_count else 0
    print chat_count
    redisDB.hset(name=chat_id, key=CHAT, value=chat_count)

def reset_chat_count(chat_id):
    redisDB.hset(name=chat_id, key=CHAT, value=0)

