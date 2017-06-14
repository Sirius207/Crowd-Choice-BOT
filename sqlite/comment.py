#!/usr/bin/python
# coding:utf-8

import json
import datetime
from config import bot_config

conn = bot_config['sqlConn']
cursor = conn.cursor()


def get_normal_answer_rat_by_chat_id(chat_id, answer_id):
    ''' check user already rat the answer'''
    sql = 'SELECT * FROM COMMENT WHERE ANSWER_ID = ? AND USER_ID = ? AND TYPE = "rat"'
    cursor.execute(sql, [answer_id, chat_id])
    rat = cursor.fetchall()
    return rat

def save_normal_answer_rat(chat_id, question_id, answer_id, reason):
    '''rat an answer'''
    time = datetime.datetime.now()
    sql = 'INSERT INTO COMMENT (QUESTION_ID, ANSWER_ID, USER_ID, CONTENT, TYPE, CREATED_AT) \
        VALUES (?,?,?,?,?,?)'
    cursor.execute(sql, [question_id, answer_id, chat_id, reason, "rat", time])
    conn.commit()

