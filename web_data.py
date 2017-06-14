

from sqlite.question import (get_question_by_ID)
from sqlite.answer import (
    get_answers_by_id, get_answers_by_answerer_id,
    update_answer_rat_by_id, get_choice_answer_rat_by_id
)
from sqlite.comment import (save_normal_answer_rat, get_normal_answer_rat_by_chat_id)
from sqlite.profile import (update_user_rat_by_id)

from hash_check import check_hash

from config import bot_config
BAN_COUNT = bot_config['BAN_COUNT']


def check_answerer_valid(question_id, chat_id, hash_value):
    ''' check user answer of question '''
    return get_answers_by_answerer_id(question_id, chat_id) and check_hash(chat_id, hash_value)


def get_full_question_by_id(question_id):
    ''' get question data '''
    question = {
        'content': get_question_by_ID(question_id),
        'answers' : get_answers_by_id(question_id)
    }
    return question

def rat_answer_by_id(chat_id, question_id, answer_id, reason):
    ''' rat answer & plus rate count '''
    if not get_normal_answer_rat_by_chat_id(chat_id, answer_id):
        # save rat reason
        save_normal_answer_rat(chat_id, question_id, answer_id, reason)
        # plus rat count
        update_answer_rat_by_id(answer_id)

        # check rat count
        if get_choice_answer_rat_by_id(answer_id) >= BAN_COUNT:
            # ban user
            update_user_rat_by_id(chat_id=chat_id, is_rat=1)
        return (True, 200)
    else:
        return (False, 400)



