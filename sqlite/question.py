#!/usr/bin/python
# coding:utf-8

import json, datetime
from config import bot_config

conn = bot_config['sqlConn']
cursor = conn.cursor()

#
# save question
#

def save_question(chat_id, question):
    ''' choose save question function by type '''
    save_by_type = {
        'choice': save_choice_question,
        'normal': save_normal_question
    }
    save_by_type[question['question_type']](chat_id, question)


def save_choice_question(chat_id, question):
    '''save choice question to Sqlite'''
    content = question['content']
    options = '\n'.join(question['options'])
    time = datetime.datetime.now()
    sql = 'INSERT INTO CHOICE_QUESTION (ASKER_ID, DESCRIPTION, OPTIONS, TYPE, CREATED_AT) \
        VALUES (?,?,?,?,?)'
    cursor.execute(sql, [chat_id, content, options, "choice", time])
    conn.commit()

def save_normal_question(chat_id, question):
    '''save choice question to Sqlite'''
    content = question['content']
    time = datetime.datetime.now()
    sql = 'INSERT INTO CHOICE_QUESTION (ASKER_ID, DESCRIPTION, TYPE, CREATED_AT) \
        VALUES (?,?,?,?)'
    cursor.execute(sql, [chat_id, content, "normal", time])
    conn.commit()

#
# get question
#

def get_new_choice_question(chat_id, question_id):
    '''get next question which not ask by current user'''
    sql = ' SELECT * \
            FROM CHOICE_QUESTION  C \
            WHERE \
                C.ASKER_ID !=  ?\
                AND C.QUESTION_ID > ?\
                AND C.RAT_COUNT < 3\
		        AND NOT EXISTS (\
                    SELECT * \
			        FROM QUESTION_ANSWER  Q\
                    WHERE   \
				        Q.ANSWERER_ID = ? \
				        AND Q.QUESTION_ID = C.QUESTION_ID\
		        ) '

    cursor.execute(sql, [chat_id, question_id, chat_id])
    questions = cursor.fetchall()

    # no more questions
    if not questions:
        return 0

    return questions[0]

def get_question_by_ID(question_id):
    '''get question by question ID'''
    sql = 'SELECT * FROM CHOICE_QUESTION WHERE QUESTION_ID = ?'
    cursor.execute(sql, [question_id])
    questions = cursor.fetchall()
    return questions[0]

def get_question_by_description(description):
    '''get question by question ID'''
    sql = 'SELECT * FROM CHOICE_QUESTION WHERE DESCRIPTION = ?'
    cursor.execute(sql, [description])
    questions = cursor.fetchall()
    return questions[0]

#
# get question text
#

def get_choice_question_text(question):
    ''' return text with question content & option '''
    options = '\n'.join(question[3].split('\n'))
    text = '問題內容為：\n '+ question[2].encode('utf-8')
    text += '"\n\n選項有:\n' + options.encode('utf-8')
    return text

def get_normal_question_text(question):
    ''' return text with question content '''
    text = '問題內容為：\n '+ question[2].encode('utf-8')
    return text

def get_choice_question_rat_by_id(question_id):
    '''get question rat by question ID'''
    sql = 'SELECT RAT_COUNT FROM CHOICE_QUESTION WHERE QUESTION_ID = ?'
    cursor.execute(sql, [question_id])
    questions = cursor.fetchall()
    return questions[0]
#
# update question rat
#

def update_question_rat_by_id(question_id):
    ''' rat question '''
    sql = 'UPDATE CHOICE_QUESTION SET RAT_COUNT = RAT_COUNT + 1  WHERE QUESTION_ID = ?'
    cursor.execute(sql, [question_id])
    conn.commit()


