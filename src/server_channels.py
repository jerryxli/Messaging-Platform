import flask
import json
from channels import channels_create_v1
from src.auth import auth_register_v1


channel_create = flask.Blueprint("channel_create", __name__)


@channel_create.route('/channels/create/v2')
def handle_channel_create():
    '''
    Replace 0 for channels_create
    with user_id received from
    JWT
    '''
    u_id = auth_register_v1("madfouni234@gmail.com", "wopooooo", "Tetian", "Madfouni2")
    data = json.loads(flask.request.data)
    channels_create_v1(0, data['name'], bool(data['is_public']))
    