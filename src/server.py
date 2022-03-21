import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.auth import auth_login_v1, auth_logout_v1, auth_register_v1
from src.user import user_profile_v1, user_setemail_v1, user_setname_v1

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
def handle_clear():
    clear_v1()
    return {}

@APP.route("/auth/register/v2", methods=['POST'])
def handle_register_v2():
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last']

    return auth_register_v1(email,password,name_first, name_last)

@APP.route("/auth/login/v2", methods=['POST'])
def handle_login_v2():
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']

    return auth_login_v1(email, password)

@APP.route("/auth/logout/v1", methods=['POST'])
def handle_logout_v1():
    request_data = request.get_json()

    token = request_data['token']

    return auth_logout_v1(token)


@APP.route("/user/profile/v1", methods=['GET'])
def handle_profile_v1():
    
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    return user_profile_v1(token, u_id)

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def handle_setname_v1():
    request_data = request.get_json()
    token = request_data['token']
    name_first = request_data['name_first']
    name_last = request_data['name_last']

    return user_setname_v1(token, name_first, name_last)

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def handle_setemail_v1():
    request_data = request.get_json()
    token = request_data['token']
    email = request_data['email']

    return user_setemail_v1(token, email)
#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
