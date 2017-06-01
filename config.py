#!/usr/bin/python
# coding:utf-8

import redis
import sqlite3

# Redis Config
redisDB = redis.StrictRedis(host='localhost', port=6379, db=0)

# question
conn = sqlite3.connect('questions.db')

# Create Question Table
conn.execute('''CREATE TABLE IF NOT EXISTS CHOICE_QUESTION(
    QUESTION_ID     INTEGER PRIMARY KEY     AUTOINCREMENT,
    ASKER_ID        INTEGER                 NOT NULL,
    DESCRIPTION     TEXT                    NOT NULL,
    OPTIONS         BLOB                    ,
    TAGS            BLOB                    ,
    TYPE            TEXT                    NOT NULL,
    CREATED_AT      TEXT                    NOT NULL,
    STARS_COUNT     BLOB                    ,
    RAT_COUNT       INTEGER DEFAULT 0);''')


# Create Answer Table
conn.execute('''CREATE TABLE IF NOT EXISTS QUESTION_ANSWER(
    ANSWER_ID       INTEGER PRIMARY KEY     AUTOINCREMENT,
    QUESTION_ID     INTEGER                 NOT NULL,
    ANSWERER_ID     INTEGER                 NOT NULL,
    ANSWER          TEXT                    NOT NULL,
    TAGS            BLOB                    ,
    TYPE            TEXT                    NOT NULL,
    CREATED_AT      TEXT                    NOT NULL,
    STARS_COUNT     BLOB                    ,
    RAT_COUNT       INTEGER DEFAULT 0);''')

# Create Personal Profile Table
conn.execute('''CREATE TABLE IF NOT EXISTS USER_PROFILE(
    USER_ID         INTEGER PRIMARY KEY     NOT NULL,
    GENDER          TEXT                    ,
    AGE             TEXT                    ,
    SUBSCRIBE       TEXT DEFAULT "On"       ,
    STATE           TEXT DEFAULT "user"     NOT NULL,
    CREATED_AT      TEXT                    NOT NULL,
    COIN            INTEGER DEFAULT 15      ,
    LEVEL           INTEGER DEFAULT 1       ,                
    CONDITION       TEXT DEFAULT "NORMAL"   ,
    RAT_COUNT       INTEGER DEFAULT 0);''')


bot_config = {
    'redisDB': redisDB,
    'sqlConn': conn,
    'API_TOKEN': '#',
    'WEBHOOK_URL': '#',
    'WELCOME_TEXT': '歡迎使用 "神奇海螺" \n 你可於此發問，或是提出問題。 每詢問一個問題會消耗五枚金幣，每回答一個問題會增加一枚金幣，祝你玩得愉快~ \n \
指令說明: \n question - Ask new question \n \
answer - Get a question and answer it \n \
info - Check Current condition \n \
mute - Mute new question notification \n \
open - Open new question notification \n \
setup - Setup User info \n',
    'HELP_TEXT': '指令說明: \n question - Ask new question \n\
 answer - Get a question and answer it \n\
 info - Check Current condition \n\
 mute - Mute new question notification \n\
 open - Open new question notification \n\
 setup - Setup User info \n',
    'age_list':[
        '< 10',
        '11 ~ 20',
        '21 ~ 30',
        '31 ~ 40',
        '41 ~ 50',
        '51 ~ 60',
        '61 ~ 70',
        '71 ~ 80',
        '81 ~ 90',
        '> 90',
    ],
    'gender_list':[
        'Male',
        'Female',
        'Others'
    ]
}
