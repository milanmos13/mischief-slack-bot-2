from mischief_db import *
from mischief_season_challenge import MischiefSlack
from slack_api import *
from time import sleep
import json

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    print("event received")
    WHITE_POINTS = 2.0
    RED_POINTS = 3.0
    BLACK_POINTS = 4.0
    THROW_POINTS = 1.0
    REGEN_POINTS = 2.0
    ALTITUDE_POINTS = 0.0
    BOT_CHANNEL = "C03UHTL3J58"
    data = request.get_json()
    if data['type'] == "url_verification":
        return jsonify({'challenge': data['challenge']})
    print('HTTP_X_SLACK_RETRY_NUM' in list(request.__dict__['environ'].keys()))
    if 'HTTP_X_SLACK_RETRY_NUM' in list(request.__dict__['environ'].keys()):
        print("Retry Number " + request.__dict__['environ']['HTTP_X_SLACK_RETRY_NUM'])
        if int(request.__dict__['environ']['HTTP_X_SLACK_RETRY_NUM']):
            return make_response("Ok", 200, )
    print(data)
    obj = MischiefSlack(data)
    if not obj._bot and not obj._reaction_added and not obj._reaction_removed:
        print("not a bot")
        obj.isRepeat()
        obj._repeat = False
        if obj._points_to_add > 0 or obj.altitude:
            print("points to add")
            obj.handle_db()
        else:
            print("executing commands")
            obj.execute_commands()

    print(obj)
    print("responding")
    return make_response("Ok", 200, )