import sys
import jwt
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import AccessError, InputError
from src import config
from src.other import clear_v1
from src.channel import channel_details_v2, is_valid_channel
from src.auth import auth_login_v1, auth_register_v1, is_valid_JWT

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    return {}

@APP.route("/auth/register/v2", methods=['POST'])
def register_v2():
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last']

    return auth_register_v1(email,password,name_first, name_last)

@APP.route("/auth/login/v2", methods=['POST'])
def login_v2():
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']

    return auth_login_v1(email, password)


# Channel Server Instructions
@APP.route("channel/details/v2", methods = ["GET"])
def handle_channel_details():
    request_data = request.args.get()
    user_jwt = request_data['token']
    channel_id = request_data['channel_id']
    if not is_valid_JWT(user_jwt):
        raise AccessError(description = 'No message specified')
    if not is_valid_channel(channel_id):
        raise InputError(description = 'No message specified')

    return channel_details_v2(user_jwt, channel_id)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
