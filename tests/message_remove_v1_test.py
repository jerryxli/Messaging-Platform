from src.config import url
import pytest
import requests

CHANNEL_JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
MESSAGE_SEND_URL = f"{url}/message/send/v1"
MESSAGE_REMOVE_URL = f"{url}/message/remove/v1"
CHANNEL_MESSAGES_URL = f"{url}/channel/messages/v2"
LEAVE_URL = f"{url}/channel/leave/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au",
                  'password': "badpassword123", 'name_first': "Ji", 'name_last': "Sun"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password",
                  'name_first': "Jane", 'name_last': "Gyuri"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


def test_normal_functionality(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"}).json()['message_id']
    # check that channel_id has messages within it
    response = requests.get(CHANNEL_MESSAGES_URL, params={'channel_id': channel_id, 'start': 0}, json = {'token': user_token_1})
    assert response.json() != {'messages': [], 'start': 0, 'end': -1}
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_1, 'message_id': message_id})
    assert response.status_code == 200
    response = requests.get(CHANNEL_MESSAGES_URL, params={'channel_id': channel_id, 'start': 0}, json = {'token': user_token_1})
    assert response.status_code == 200
    # check that channel_id has no messages within it
    assert response.json() == {'messages': [], 'start': 0, 'end': -1}


def test_message_already_removed(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"}).json()['message_id']
    # check that channel_id has messages within it
    response = requests.get(CHANNEL_MESSAGES_URL, params={'channel_id': channel_id, 'start': 0}, json = {'token': user_token_1})
    assert response.json() != {'messages': [], 'start': 0, 'end': -1}
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_1, 'message_id': message_id})
    # check that channel_id has NO messages within it
    assert response.status_code == 200
    response = requests.get(CHANNEL_MESSAGES_URL, params={'channel_id': channel_id, 'start': 0}, json = {'token': user_token_1})
    assert response.status_code == 200
    assert response.json() == {'messages': [], 'start': 0, 'end': -1}
    # attempt to remove the message again
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_1, 'message_id': message_id})
    assert response.status_code == 400


def test_message_id_invalid(clear_store, create_user):
    user_token_1 = create_user['token']
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_1, 'message_id': 100})
    assert response.status_code == 400


def test_user_id_didnt_send_message(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})  
    assert response.status_code == 200
    message_id = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"}).json()['message_id']
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_2, 'message_id': message_id})
    assert response.status_code == 403

def test_user_without_permissions(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})  
    assert response.status_code == 200
    message_id = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_2, 'channel_id': channel_id, 'message': "Leo loves coding!"}).json()['message_id']
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_2, 'message_id': message_id})
    assert response.status_code == 200

def test_user_leaves_channel(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    message_id = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"}).json()['message_id']
    response = requests.post(LEAVE_URL, json = {'token': user_token_1, 'channel_id': channel_id})
    response = requests.delete(MESSAGE_REMOVE_URL, json = {'token': user_token_1, 'message_id': message_id})
    assert response.status_code == 400