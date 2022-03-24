import sys
import jwt
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import AccessError, InputError
from src import config
from src.other import clear_v1, user_id_from_JWT
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_leave_v1, channel_messages_v1, channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_login_v1, auth_logout_v1, auth_register_v1, is_valid_JWT
from src.user import user_profile_v1, user_setemail_v1, user_setname_v1, users_all_v1, user_remove_v1
from src.message import message_send_v1
from src.dm import dm_create_v1, dm_list_v1



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

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

@APP.route("/clear/v1", methods=['DELETE'])
def handle_clear():
    clear_v1()
    return {}

# Auth Server Instructions

@APP.route("/auth/register/v2", methods=['POST'])
def handle_register_v2():
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last']

    return auth_register_v1(email, password, name_first, name_last)


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

# User Server Instructions

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

@APP.route("/users/all/v1", methods = ['GET'])
def handle_users_all_v1():
    print("WHYYYYY")
    user_token= request.args.get('token')
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return users_all_v1(user_id)
# Channels Server Instructions

@APP.route("/channels/create/v2", methods=["POST"])
def handle_channels_create_v2():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_name = request_data['name']
    is_public = request_data['is_public']
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return channels_create_v1(user_id, channel_name, is_public)


@APP.route("/channels/list/v2", methods=["GET"])
def handle_channels_list_v2():
    user_token = request.args.get('token')
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return channels_list_v1(user_id)

@APP.route("/channels/listall/v2", methods=['GET'])
def handle_channels_listall_v2():
    user_token = request.args.get('token')
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return channels_listall_v1(user_id)

# Channel Server Instructions


@APP.route("/channel/details/v2", methods=["GET"])
def handle_channel_details():
    user_token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return channel_details_v1(user_id, channel_id)


@APP.route("/channel/join/v2", methods=["POST"])
def handle_channel_join():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = request_data['channel_id']
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    channel_join_v1(user_id, channel_id)
    return {}

@APP.route("/channel/invite/v2", methods=['POST'])
def handle_channel_invite():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = request_data['channel_id']
    u_id = int(request_data['u_id'])
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    channel_invite_v1(user_id, channel_id, u_id)
    return {}

@APP.route("/channel/leave/v1", methods=['POST'])
def handle_channel_leave():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = int(request_data['channel_id'])
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    channel_leave_v1(user_id, channel_id)
    return {}

@APP.route("/channel/addowner/v1", methods = ["POST"])
def handle_channel_addowner():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = int(request_data['channel_id'])
    u_id = int(request_data['u_id'])
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    channel_addowner_v1(user_id, channel_id, u_id)
    return {}

@APP.route("/channel/messages/v2", methods=['GET'])
def handle_channel_messages():
    user_token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return channel_messages_v1(user_id, channel_id, start)

    
@APP.route("/channel/removeowner/v1", methods = ["POST"])
def handle_channel_removeowner():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = int(request_data['channel_id'])
    u_id = int(request_data['u_id'])
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    channel_removeowner_v1(user_id, channel_id, u_id)
    return {}

# Message Server Instructions
@APP.route("/message/send/v1", methods = ['POST'])
def handle_message_send():
    request_data = request.get_json()
    user_token = request_data['token']
    channel_id = int(request_data['channel_id'])
    message = request_data['message']
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return message_send_v1(user_id, channel_id, message) 

# DM Server Instructions
@APP.route("/dm/create/v1", methods = ["POST"])
def handle_dm_create():
    request_data = request.get_json()
    user_token = request_data['token']
    u_ids = request_data['u_ids']
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return dm_create_v1(user_id, u_ids)

@APP.route("/dm/list/v1", methods = ["GET"])
def handle_dm_list():
    user_token = request.args.get('token')
    if not is_valid_JWT(user_token):
        raise AccessError("JWT no longer valid")
    user_id = user_id_from_JWT(user_token)
    return dm_list_v1(user_id)

@APP.route("/admin/user/remove/v1", methods = ["DELETE"])
def handle_user_remove():
    print("THANKS XXXXX")
    request_data = request.get_json()
    print(request_data)
    if not is_valid_JWT(request_data['token']):
        raise AccessError
    return user_remove_v1(request_data['token'], request_data['u_id'])

# NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port
