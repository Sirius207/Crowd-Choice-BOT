#!/usr/bin/python
# coding:utf-8

import json, datetime
from config import bot_config

conn = bot_config['sqlConn']
cursor = conn.cursor()

COIN_ADD = 1
COIN_SUB = -5

#
# get user data
#

def get_user_by_id(chat_id):
    sql = 'SELECT * FROM USER_PROFILE WHERE USER_ID = ?'
    cursor.execute(sql, [chat_id])
    user = cursor.fetchall()
    # no this user
    if not user:
        return 0

    return user[0]

def get_available_users_id_list():
    ''' get user id list '''
    sql = 'SELECT USER_ID FROM USER_PROFILE WHERE SUBSCRIBE != "Off" AND STATE = "user" '
    cursor.execute(sql)
    users = cursor.fetchall()
    return users

def get_user_state_by_id(chat_id):
    ''' get user state '''
    sql = 'SELECT STATE FROM USER_PROFILE WHERE USER_ID = ?'
    cursor.execute(sql, [chat_id])
    state = cursor.fetchall()
    # no this user
    if not state:
        return 0
    return state[0][0]

def get_user_coin_by_id(chat_id):
    ''' get user state '''
    sql = 'SELECT COIN FROM USER_PROFILE WHERE USER_ID = ?'
    cursor.execute(sql, [chat_id])
    coin = cursor.fetchall()
    # no this user
    if not coin:
        return 0
    return coin[0][0]


def get_question_counts(chat_id):
    ''' get counts of questions asked by user'''
    sql = 'SELECT COUNT (QUESTION_ID) FROM CHOICE_QUESTION WHERE ASKER_ID = ?'
    cursor.execute(sql, [chat_id])
    counts = cursor.fetchall()
    return counts[0][0]

def get_answer_counts(chat_id):
    ''' get counts of answers asked by user'''
    sql = 'SELECT COUNT (ANSWER_ID) FROM QUESTION_ANSWER WHERE ANSWERER_ID = ?'
    cursor.execute(sql, [chat_id])
    counts = cursor.fetchall()
    return counts[0][0]

def get_user_profile_text(chat_id):
    ''' send back user condition '''
    user = get_user_by_id(chat_id)
    coin = user[5]
    level = user[6]
    question_counts = get_question_counts(chat_id)
    answers_counts = get_answer_counts(chat_id)
    text = '您目前：\n'
    text += '已提出: ' + str(question_counts) + ' 則問題\n'
    text += '已回答: ' +  str(answers_counts) + '則問題\n\n'
    text += '還有 ' + str(coin) + ' 枚金幣\n'
    text += '等級為 ' + str(level) + ' !'
    return text


#
# setup
#

def create_new_user(chat_id):
    '''create user to Sqlite'''
    time = datetime.datetime.now()
    sql = 'INSERT INTO USER_PROFILE (USER_ID, CREATED_AT) VALUES (?,?)'
    cursor.execute(sql, [chat_id, time])
    conn.commit()

def save_age_profile(chat_id, age):
    '''save user age to Sqlite'''
    sql = 'UPDATE USER_PROFILE SET AGE = ?  WHERE USER_ID = ?;'
    cursor.execute(sql, [age, chat_id])
    conn.commit()

def save_gender_profile(chat_id, gender):
    '''save user gender to Sqlite'''
    sql = 'UPDATE USER_PROFILE SET GENDER = ?  WHERE USER_ID = ?;'
    cursor.execute(sql, [gender, chat_id])
    conn.commit()

def update_user_state_by_id(chat_id, state):
    '''save current state of user'''
    sql = 'UPDATE USER_PROFILE SET STATE = ?  WHERE USER_ID = ?;'
    cursor.execute(sql, [state, chat_id])
    conn.commit()

def update_user_subscribe_by_id(chat_id, is_subscribe):
    '''save current state of user'''
    sql = 'UPDATE USER_PROFILE SET SUBSCRIBE = ?  WHERE USER_ID = ?;'
    cursor.execute(sql, [is_subscribe, chat_id])
    conn.commit()


def update_user_coin_by_id(chat_id, is_add):
    '''save current state of user'''
    add_number = COIN_ADD if is_add else COIN_SUB
    sql = 'UPDATE USER_PROFILE SET COIN = COIN + ?  WHERE USER_ID = ?;'
    cursor.execute(sql, [add_number, chat_id])
    conn.commit()






