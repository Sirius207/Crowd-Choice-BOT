#!/usr/bin/python
# coding:utf-8

import json
import datetime
from config import bot_config

conn = bot_config['sqlConn']
cursor = conn.cursor()


def save_choice_answer(chat_id, question_id, answer):
    '''save choice question to Sqlite'''
    time = datetime.datetime.now()

    sql = 'INSERT INTO QUESTION_ANSWER (QUESTION_ID, ANSWERER_ID , ANSWER, TYPE, CREATED_AT) \
        VALUES (?,?,?,?,?)'
    cursor.execute(sql, [question_id, chat_id, answer, "choice", time])
    conn.commit()


def get_choice_answer(question_id):
    ''' get question answers list'''
    sql = 'SELECT  ANSWER from QUESTION_ANSWER WHERE QUESTION_ID == ?'
    cursor.execute(sql, [question_id])
    conn.commit()
    answers = cursor.fetchall()
    return answers


def get_choice_answer_statistics(question_id):
    ''' get question answers statics'''
    statistics = dict()
    answers = get_choice_answer(question_id)
    for element in enumerate(answers):
        if element[1] in statistics:
            statistics[element[1]] += 1
        else:
            statistics[element[1]] = 1

    return statistics


def generate_answer_statistics_html(question_id):
    '''get statics text'''
    answer = get_choice_answer_statistics(question_id)
    text = '<b>目前回答統計結果為：</b>\n\n'
    for key in answer:
        option = key[0].encode('utf-8') + ': ' + str(answer[key]) + ' 人 \n'
        text += option

    return text
