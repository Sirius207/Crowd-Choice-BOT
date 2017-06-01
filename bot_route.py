
from machine import machine
from get_message_info import get_text, get_chat_id
from sqlite.profile import (get_user_state_by_id, update_user_state_by_id)

command = {
    '/start': machine.start,
    '/setup': machine.setup,
    '/info': machine.info,
    '/mute': machine.mute,
    '/open': machine.open,
    '/answer': machine.answer,
    '/old_question': machine.old_question
}


def bot_route(update):
    ''' bot process '''
    user_state = get_user_state_by_id(get_chat_id(update))
    # move to user state
    machine.state = user_state

    # execute command
    try:
        command[get_text(update)](update)
    except KeyError:
        machine.advance(update)

    # save user current state to Sqlite
    update_user_state_by_id(get_chat_id(update), machine.state)

    # reset the system state for next user
    machine.state = 'user'


