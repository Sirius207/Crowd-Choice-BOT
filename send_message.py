#!/usr/bin/python
# coding:utf-8

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from get_message_info import (get_text, get_first_name, get_chat_id)

import hashlib

from redisDB.temp_question import (
    save_broadcast_question_ID
)

from sqlite.question import (
    get_choice_question_text, get_normal_question_text, 
    get_question_by_description, get_question_by_ID
)


from sqlite.answer import (
    save_answer, save_choice_answer_rat, get_choice_answer_statistics,
    generate_answer_statistics_html, get_choice_answer, get_answer_by_answer_id
)

from sqlite.profile import (
    get_user_by_id, get_available_users_id_list, get_user_profile_text,
    update_user_coin_by_id, get_user_coin_by_id, update_user_state_by_id
)


from config import bot_config
API_TOKEN = bot_config['API_TOKEN']
bot = telegram.Bot(token=API_TOKEN)
INDEX_URL = bot_config['INDEX_URL']
HASHKEY = bot_config['HASHKEY']

def build_menu(buttons,
               n_cols,
               header_buttons,
               footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def send_question(chat_id, question):
    '''send new question to single user'''
    print 'send question'
    # generate keyboard
    button_list = [
        InlineKeyboardButton("跳過", callback_data="answer-pass"),
        InlineKeyboardButton("取消回答", callback_data="answer-cancel"),
        InlineKeyboardButton("這問題不適當", callback_data="answer-rat"),
    ]

    # generate message
    text = '您有一則新問題，ID:'
    text += str(question[0]) + '\n'
    # check button list
    question_type = question[5]
    if question_type == 'choice':
        for index, element in enumerate(question[3].split('\n')):
            button_list.append(InlineKeyboardButton(
                element, callback_data=element))

        text += get_choice_question_text(question)
        text += '\n\n請直接點選選項回答~'
    else:
        text += get_normal_question_text(question)
        text += '\n\n請直接輸入您的回答，或點選選項~'

    reply_markup = InlineKeyboardMarkup(
        build_menu(
            button_list,
            n_cols=3,
            header_buttons=None,
            footer_buttons=None
        )
    )

    bot.send_message(chat_id=chat_id,
                     text=text, reply_markup=reply_markup)


def broadcast_question(question):
    ''' broadcast new question to avaliable user'''
    users_id_list = get_available_users_id_list()
    full_question = get_question_by_description(question['content'])
    print (users_id_list)
    for index, element in enumerate(users_id_list):
        # send new question messgage
        send_question(element[0], full_question)
        # save current question for that user
        save_broadcast_question_ID(element[0], full_question[0])
        update_user_state_by_id(element[0], 'state2')


def handle_answer(update, question):
    ''' check question type '''
    question_type = question[5]
    handle_answer_type = {
        'choice': handle_choice_answer,
        'normal': handle_normal_answer
    }
    return handle_answer_type[question_type](update, question)

def handle_normal_answer(update, question):
    ''' check answer & send response & send answers'''
    # send basic message
    send_basic_answer_response(update, question)

    # setup answer route
    hash_value = str(get_chat_id(update)) + HASHKEY
    link = INDEX_URL + 'question/' + str(question[0]) + '?user=' + str(get_chat_id(update))
    link += '&hash=' + hashlib.sha224(hash_value).hexdigest()
    # send answers link to answerer
    text = '可以從 <a href="'
    text += link
    text += '">這裡</a> 查看其他人的回答～'
    bot.send_message(chat_id=get_chat_id(update),
                     text=text,
                     parse_mode=telegram.ParseMode.HTML)

    asker_subscribe = get_user_by_id(question[1])[3]
    if asker_subscribe == 'On':
        text = '您的問題： ' + question[2].encode('utf-8') + '\n' + text
        bot.send_message(chat_id=question[1],
                         text=text,
                         parse_mode=telegram.ParseMode.HTML)

    return True


def handle_choice_answer(update, question):
    '''check answer & send response & send statistics'''
    question_id = question[0]
    print question
    print 'id'
    print question_id
    # check answer is valid
    if get_text(update) not in question[3].split('\n'):
        text = "請直接點選底下的按鈕進行回答！"
        bot.send_message(get_chat_id(update), text)
        return False
    else:
        # send basic message
        send_basic_answer_response(update, question)
        # send statistics message
        text = generate_answer_statistics_html(question_id)
        bot.send_message(
            chat_id=get_chat_id(update), text=text,
            parse_mode=telegram.ParseMode.HTML
        )

        # send statistics back to ori asker each 5 answer
        asker_subscribe = get_user_by_id(question[1])[3]
        answers_count = len(get_choice_answer(question_id))
        if answers_count % 5 == 0 and asker_subscribe == 'On':
            text = get_choice_question_text(question) + '\n' + text
            bot.send_message(
                chat_id=question[1], text=text,
                parse_mode=telegram.ParseMode.HTML
            )

        return True

def send_basic_answer_response(update, question):
    ''' save answer & send message & add coin '''
    # save answer to Sqlite
    save_answer(chat_id=get_chat_id(update), question_id=question[0],
                answer=get_text(update), question_type=question[5])

    # send first message
    text = get_text(update).encode('utf-8') + ', 已收到您的回答! 金幣數加 1!'
    bot.send_message(get_chat_id(update), text)

    # add coin
    update_user_coin_by_id(chat_id=get_chat_id(update), is_add=1)
    text = '目前金幣數為：' + \
        str(get_user_coin_by_id(get_chat_id(update))) + ' ~~'
    bot.send_message(get_chat_id(update), text)


def send_rat_question_warning(question_id, reason):
    ''' send warning to asker'''
    question = get_question_by_ID(question_id)
    text = '您先前提出的問題：' + question[2].encode('utf-8')
    text += '\n因為 ' + reason.encode('utf-8') + ' 被檢舉囉~ 請注意~~'
    bot.send_message(chat_id=question[1], text=text)


def send_rat_answer_warning(answer_id, reason):
    ''' send warning to answerer '''
    answer = get_answer_by_answer_id(answer_id)
    text = '您先前的回答：' + answer[3].encode('utf-8')
    text += '\n因為 ' + reason.encode('utf-8') + ' 被檢舉囉~ 請注意~~'
    bot.send_message(chat_id=answer[2], text=text)

