import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file, render_template
from machine import machine
from config import bot_config
from bot_route import bot_route
from web_data import ( get_full_question_by_id, check_answerer_valid)

API_TOKEN = bot_config['API_TOKEN']
WEBHOOK_URL = bot_config['WEBHOOK_URL']

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    bot_route(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

@app.route('/question/<question_id>', methods=['GET'])
def show_normal_answer(question_id=None):
    chat_id = request.args.get('user')
    if not check_answerer_valid(question_id, chat_id):
        print 'not valid user'
        return render_template('warn.html')
    else:
        question = get_full_question_by_id(question_id, chat_id)
        return render_template('question.html', question=question)

if __name__ == "__main__":
    _set_webhook()
    app.run()
