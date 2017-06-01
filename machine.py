from fsm import TocMachine

machine = TocMachine(
    states=[
        'user',
        'config_age',
        'config_gender',
        'state1',
        'state3',
        'state4',
        'state2',
    ],
    transitions=[
        # initial setup
        {
            'trigger': 'start',
            'source': 'user',
            'dest': 'temp',
            'conditions': 'is_new_user'
        },
        {
            'trigger': 'info',
            'source': 'user',
            'dest': 'temp',
            'conditions': 'send_info'
        },
        {
            'trigger': 'mute',
            'source': 'user',
            'dest': 'temp',
            'conditions': 'mute_receive_question'
        },
        {
            'trigger': 'open',
            'source': 'user',
            'dest': 'temp',
            'conditions': 'open_receive_question'
        },
        {
            'trigger': 'setup',
            'source': 'user',
            'dest': 'config_age',
            'conditions': 'is_going_to_config_age'
        },
        {
            'trigger': 'advance',
            'source': 'config_age',
            'dest': 'config_gender',
            'conditions': 'is_valid_age_input'
        },
        {
            'trigger': 'advance',
            'source': 'config_gender',
            'dest': 'user',
            'conditions': 'is_valid_gender_input'
        },
        # ask question process
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'go_back',
            'source': '*',
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state3',
        },
        {
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state4',
        },
        {
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'user',
            'conditions': 'is_correct'
        },
        {
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'user',
            'conditions': 'is_not_correct'
        },
        {
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'state1',
            'conditions': 'is_edit'
        },
        # answer process
        {
            'trigger': 'answer',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'user',
            'conditions': 'is_valid_answer'
        },
        {
            'trigger': 'new_question',
            'source': 'state2',
            'dest': 'state2',
        },
        {
            'trigger': 'old_question',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'reset_current_question'
        },
    ],
    initial='user',
    auto_transitions=True,
    show_conditions=True,
)