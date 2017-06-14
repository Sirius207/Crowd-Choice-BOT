#!/usr/bin/python
# coding:utf-8

import json
from config import bot_config

redisDB = bot_config['redisDB']

TEMP = 'temp_question'
CURR = 'current_question'

#
# Question
#
def save_temp_question(chat_id, question):
    '''temp save question to Redis'''
    to_save_question = {'content': question}
    redisDB.hset(name=chat_id, key=TEMP, value=json.dumps(to_save_question))
    print ('save question success')

def get_temp_question(chat_id):
    '''get temp question in Redis'''
    return json.loads(redisDB.hget(name=chat_id, key=TEMP))

def remove_temp_question(chat_id):
    '''delete temp question in Redis'''
    redisDB.hdel(chat_id, TEMP)
    print ('delete question success')

#
# Options of Question
#

def set_temp_options(chat_id, options):
    ''' set option value in dict question'''
    question = get_temp_question(chat_id)
    question['options'] = options
    return question

def save_temp_options(chat_id, options):
    '''temp save question to Redis'''
    question = set_temp_options(chat_id, options)
    redisDB.hset(name=chat_id, key=TEMP, value=json.dumps(question))
    print ('save options success')

#
# Type of Question
#

def set_temp_question_type(chat_id, question_type):
    ''' set type value in dict question'''
    question = get_temp_question(chat_id)
    question['question_type'] = question_type
    return question

def save_temp_question_type(chat_id, question_type):
    '''temp save question to Redis'''
    question = set_temp_question_type(chat_id, question_type)
    redisDB.hset(name=chat_id, key=TEMP, value=json.dumps(question))
    print ('save type success')

#
# Generate question
#

def get_temp_question_html(chat_id):
    '''return question & options with html format '''
    question_data =  get_temp_question(chat_id)
    question_content = question_data['content'].encode('utf-8')
    question_options = question_data['options']
    question_type    = question_data['question_type']
    question = '<b>Q: \n' + question_content  + '</b>\n\n'

    if question_type == 'choice':
        question += 'A:\n'
        for index, element in enumerate(question_options):
            question += '(' + str(index + 1) + ') ' + element.encode('utf-8') + '\n'

    return question


#
# save current question
#
def save_current_question_ID(chat_id, question_id):
    '''temp save question to Redis'''
    to_save_question = {'question_ID': question_id}
    redisDB.hset(name=chat_id, key=CURR, value=json.dumps(to_save_question))
    print ('save question id success')


def save_broadcast_question_ID(chat_id, question_id):
    '''temp save broadcast question to Redis'''
    to_save_question = json.loads(redisDB.hget(name=chat_id, key=CURR))
    to_save_question['broadcast_question_ID'] = question_id
    redisDB.hset(name=chat_id, key=CURR, value=json.dumps(to_save_question))
    print ('save broadcast question id success')

def reset_current_question_ID(chat_id):
    ''' reset current question_id '''
    to_save_question = json.loads(redisDB.hget(name=chat_id, key=CURR))
    to_save_question['question_ID'] = 0
    redisDB.hset(name=chat_id, key=CURR, value=json.dumps(to_save_question))
    print ('reset question id success')

def reset_broadcast_question_ID(chat_id):
    ''' reset current question_id '''
    to_save_question = json.loads(redisDB.hget(name=chat_id, key=CURR))
    to_save_question['broadcast_question_ID'] = 0
    redisDB.hset(name=chat_id, key=CURR, value=json.dumps(to_save_question))
    print ('reset broadcast question id success')


def get_current_question_ID(chat_id):
    '''get temp options in Redis'''
    if redisDB.hget(name=chat_id, key=CURR):
        question = json.loads(redisDB.hget(name=chat_id, key=CURR))
        key = 'broadcast_question_ID'
        if key in question and question['broadcast_question_ID'] != 0:
            return question['broadcast_question_ID']
        else:
            return question['question_ID']

    return 0

