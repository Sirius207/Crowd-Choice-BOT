
from sqlite.question import (get_question_by_ID)
from sqlite.answer import (get_answers_by_id, get_answers_by_answerer_id)


def check_answerer_valid(question_id, chat_id):
    ''' check user answer of question '''
    return get_answers_by_answerer_id(question_id, chat_id)


def get_full_question_by_id(question_id, chat_id):
    ''' get question data '''

    question = {
        'content': get_question_by_ID(question_id),
        'answers' : get_answers_by_id(question_id)
    }
    return question
