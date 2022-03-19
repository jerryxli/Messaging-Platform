import sys
import jwt
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import AccessError, InputError
from src import config
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, is_valid_JWT
from src.channels import channels_list_v1

JWT_SECRET = "COMP1531_H13A_CAMEL"

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

# Auth Server Instructions

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

# Channels Server Instructions

@APP.route("channels/list/v2", methods = ["GET"])
def handle_channels_list_v2():
    data = request.args.get('token')
    if not is_valid_JWT(data):
        raise AccessError(description = 'No message specified')
    jwt_payload = jwt.decode(data, JWT_SECRET, algorithms=['HS256'])
    user_id = jwt_payload['auth_user_id']

    return channels_list_v1(user_id)


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
