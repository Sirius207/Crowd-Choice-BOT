#!/usr/bin/python
# coding:utf-8

from transitions.extensions import GraphMachine

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


from get_message_info import (get_text, get_first_name, get_chat_id)

from redisDB.temp_question import *

from sqlite.question import (
    save_choice_question, get_new_choice_question, get_choice_question_by_description,
    get_choice_question_by_ID, get_choice_question_text
)
from sqlite.answer import (
    save_choice_answer, get_choice_answer_statistics,
    generate_answer_statistics_html, get_choice_answer
)
from sqlite.profile import (
    get_user_by_id, get_available_users_id_list, get_user_profile_text,
    create_new_user, save_gender_profile, save_age_profile, update_user_state_by_id,
    update_user_subscribe_by_id, update_user_coin_by_id, get_user_coin_by_id
)

from config import bot_config
AGE_LIST = bot_config['age_list']
GENDER_LIST = bot_config['gender_list']
WELCOME_TEXT = bot_config['WELCOME_TEXT']
HELP_TEXT = bot_config['HELP_TEXT']

API_TOKEN = bot_config['API_TOKEN']
bot = telegram.Bot(token=API_TOKEN)


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
    # generate keyboard
    button_list = [
        InlineKeyboardButton("跳過", callback_data="answer-pass"),
        InlineKeyboardButton("取消回答", callback_data="answer-cancel"),
        InlineKeyboardButton("這問題不適當", callback_data="answer-rat"),
    ]
    for index, element in enumerate(question[3].split('\n')):
        button_list.append(InlineKeyboardButton(element, callback_data=element))
    reply_markup = InlineKeyboardMarkup(
        build_menu(
            button_list,
            n_cols=3,
            header_buttons=None,
            footer_buttons=None
        )
    )

    # generate message
    text = '您有一則新問題，' + get_choice_question_text(question)
    text += '\n\n請直接點選選項回答~'
    bot.send_message(chat_id=chat_id,
                     text=text, reply_markup=reply_markup)



def broadcast_question(question):
    ''' broadcast new question to avaliable user'''
    users_id_list = get_available_users_id_list()
    full_question = get_choice_question_by_description(question['content'])
    print (users_id_list)
    for index, element in enumerate(users_id_list):
        # send new question messgage
        send_question(element[0], full_question)
        # save current question for that user
        save_broadcast_question_ID(element[0], full_question[0])
        update_user_state_by_id(element[0], 'state2')


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # ========================================================
    # Setup user info
    # ========================================================

    def is_new_user(self, update):
        if get_user_by_id(get_chat_id(update)) == 0:
            create_new_user(get_chat_id(update))
            text = WELCOME_TEXT
            bot.send_message(get_chat_id(update), text)
        else:
            text = HELP_TEXT
            bot.send_message(get_chat_id(update), text)

        return False

    def is_going_to_config_age(self, update):
        print ('check is_going_to_config_age')
        text = get_text(update)
        return text.lower() == '/setup'

    def is_valid_age_input(self, update):
        print ('check resolve_age_input')
        if get_text(update) in AGE_LIST:
            save_age_profile(get_chat_id(update), get_text(update))
            text = "年齡已設定為 " + get_text(update).encode('utf-8')
            bot.send_message(get_chat_id(update), text)
            return True
        else:
            text = get_text(update).encode('utf-8') + " 不是有效年齡，請直接點選底下的年齡按鈕！"
            bot.send_message(get_chat_id(update), text)
            return False

    def is_valid_gender_input(self, update):
        print ('check is_going_to_config_gender')
        if get_text(update) in GENDER_LIST:
            save_gender_profile(get_chat_id(update), get_text(update))
            text = "性別已設定為 " + get_text(update).encode('utf-8')
            bot.send_message(get_chat_id(update), text)
            return True
        else:
            text = "請直接點選底下的性別按鈕進行設定！"
            bot.send_message(get_chat_id(update), text)
            return False

    def send_info(self, update):
        text = get_user_profile_text(get_chat_id(update))
        bot.send_message(get_chat_id(update), text)
        return False

    def mute_receive_question(self, update):
        is_subscribe = 'Off'
        update_user_subscribe_by_id(get_chat_id(update), is_subscribe)
        text = '已關閉新問題通知！ 輸入/open 可重新開啟~'
        bot.send_message(get_chat_id(update), text)
        return False

    def open_receive_question(self, update):
        is_subscribe = 'On'
        update_user_subscribe_by_id(get_chat_id(update), is_subscribe)
        text = '已開啟新問題通知! 輸入/mute 可重新關閉~'
        bot.send_message(get_chat_id(update), text)
        return False

    def reset_current_question(self, update):
        reset_current_question_ID(get_chat_id(update))
        return True

    # ========================================================
    # Condition
    # ========================================================

    #
    # check quick response
    #

    def is_correct(self, update):
        print ('check question is correct')
        return get_text(update).lower() == 'yes'

    def is_not_correct(self, update):
        print ('check question is not correct')
        return get_text(update).lower() == 'no'

    def is_edit(self, update):
        print ('check question is edit')
        return get_text(update).lower() == 'edit'

    #
    # check normal input
    #

    def is_going_to_state1(self, update):
        print ('check state1')
        coin = get_user_coin_by_id(get_chat_id(update))
        if coin - 5 < 0:
            text = "問一次問題要消耗五枚金幣，目前金幣數為 " + str(coin) + ' 枚，'
            text += "多回答問題來累積金幣吧~~" 
            bot.send_message(get_chat_id(update), text)
            return False
        return get_text(update).lower() == '/question'

    def is_going_to_state2(self, update):
        print ('check state2')
        return get_text(update).lower() == '/answer'

    def is_going_to_user(self, update):
        print ('check user')
        return get_text(update).lower() != ('/question' or '/answer')


    def is_valid_answer(self, update):
        if get_text(update) == 'answer-pass':
            # remove broadcast question
            reset_broadcast_question_ID(get_chat_id(update))
            self.new_question(update)
        elif get_text(update) == 'answer-cancel':
            # remove broadcast question
            reset_broadcast_question_ID(get_chat_id(update))
            self.go_back(update)
        else:
            question_id = get_current_question_ID(get_chat_id(update))
            question = get_choice_question_by_ID(question_id)
            # check answer is valid
            if get_text(update) not in question[3].split('\n'):
                text = "請直接點選底下的按鈕進行回答！"
                bot.send_message(get_chat_id(update), text)
            else:
                # save answer to sqlite
                save_choice_answer(get_chat_id(update), question_id, get_text(update))

                # send first message
                text = get_text(update).encode('utf-8') + ', 已收到您的回答! 金幣數加 1!'
                bot.send_message(get_chat_id(update), text)

                # add coin
                update_user_coin_by_id(chat_id=get_chat_id(update), is_add=1)
                text = '目前金幣數為：' + str(get_user_coin_by_id(get_chat_id(update))) + ' ~~'
                bot.send_message(get_chat_id(update), text)

                # send statistics message
                text = generate_answer_statistics_html(question_id)
                bot.send_message(
                    chat_id=get_chat_id(update), text=text,
                    parse_mode=telegram.ParseMode.HTML
                )

                # send statistics back to ori asker
                answers_count = len(get_choice_answer(question_id))
                if answers_count%5 == 0:
                    text = get_choice_question_text(question) + '\n' + text
                    bot.send_message(
                        chat_id=question[1], text=text,
                        parse_mode=telegram.ParseMode.HTML
                    )

                # remove broadcast question
                reset_broadcast_question_ID(get_chat_id(update))
                self.go_back(update)

    # ========================================================
    # Enter & Exit State
    # ========================================================

    #
    # config age
    #

    def on_enter_config_age(self, update):
        bot.send_message(
            chat_id=get_chat_id(update),
            text="請選擇您的年齡～",
            reply_markup=telegram.ReplyKeyboardMarkup([AGE_LIST])
        )

    def on_exit_config_age(self, update):
        print ('Leaving config_age')

    def on_enter_config_gender(self, update):
        bot.send_message(
            chat_id=get_chat_id(update),
            text="請選擇您的性別～",
            reply_markup=telegram.ReplyKeyboardMarkup([GENDER_LIST])
        )

    def on_exit_config_gender(self, update):
        print ('Leaving config_gender')

    #
    # user (initial)
    #

    def on_enter_user(self, update):
        print (get_chat_id(update))
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(
            chat_id=get_chat_id(update),
            text="請輸入/question 發問，或/answer 回答問題~~",
            reply_markup=reply_markup
        )

    def on_exit_user(self, update):
        print ('Leaving user')

    #
    # state1
    #

    def on_enter_state1(self, update):
        bot.send_message(
            chat_id=get_chat_id(update),
            text="請輸入您的問題~ "
            + get_first_name(update).encode('utf-8')
            + " 同學 > w <")

    def on_exit_state1(self, update):
        print ('Leaving state1')

    #
    # state3
    #
    def on_enter_state3(self, update):
        # save question
        text = get_text(update)
        save_temp_question(chat_id=get_chat_id(update), question=text)
        # send message
        text = "請繼續輸入問題的選項，一行為一個選項 (可輸入shift + enter 換行)，最多可輸入四個～"
        bot.send_message(chat_id=get_chat_id(update), text=text)

    def on_exit_state3(self, update):
        print ('Leaving state3')

    #
    # state4
    #
    def on_enter_state4(self, update):
        # save option in redis
        options = get_text(update).split('\n')
        save_temp_options(get_chat_id(update), options)

        # prepare send message
        button_list = [
            InlineKeyboardButton("取消發問", callback_data="no"),
            InlineKeyboardButton("是的，提交", callback_data="yes"),
            InlineKeyboardButton("編輯問題", callback_data="edit")
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(
                button_list,
                n_cols=3,
                header_buttons=None,
                footer_buttons=None
            )
        )
        text = "您要提交的是下列問題嗎?"
        question = get_temp_question_html(get_chat_id(update))
        bot.send_message(chat_id=get_chat_id(update), text=text)
        bot.send_message(
            chat_id=get_chat_id(update), text=question,
            parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup
        )

    def on_exit_state4(self, update):
        if update.callback_query.data == 'yes':

            # send message
            new_question = get_temp_question(get_chat_id(update))
            save_choice_question(get_chat_id(update), new_question)
            text = "收到，您的問題已送出～請靜候其他同學的回覆. . . . .\n 每五人回覆問題時會通知一次~"

            # cost coin
            update_user_coin_by_id(chat_id=get_chat_id(update), is_add=0)

            # broadcast new question
            broadcast_question(new_question)

            # remove redis question
            remove_temp_question(get_chat_id(update))

        elif update.callback_query.data == 'no':
            remove_temp_question(get_chat_id(update))
            text = "好，歡迎下次再發問～"

        else:
            text = "現在您可以再重新輸入一次您的問題～"

        bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text=text
        )
        print ('Leaving state4')

    #
    # state2
    #

    def on_enter_state2(self, update):    
        # get new question
        question_id = get_current_question_ID(get_chat_id(update))
        print (question_id)
        question = get_new_choice_question(get_chat_id(update), question_id)
        if question == 0:
            text = '目前還沒有新問題！ 輸入/old 可重新呼叫跳過的舊問題~'
            bot.send_message(chat_id=get_chat_id(update), text=text)
            self.go_back(update)
        else:
            # save current question
            save_current_question_ID(get_chat_id(update), question[0])

            # send question
            send_question(get_chat_id(update), question)


    def on_exit_state2(self, update):
        print ('Leaving state2')

