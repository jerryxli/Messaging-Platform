from src.config import url
import pytest
import requests
from src.other import is_valid_dictionary_output

CHANNEL_JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
CHANNEL_MESSAGES_URL = f"{url}/channel/messages/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
MESSAGE_SEND_URL = f"{url}/message/send/v1"

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
                               
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"})
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {'message_id': int})
    response = requests.get(CHANNEL_MESSAGES_URL, params={'token': user_token_1,
                                                              'channel_id': channel_id, 'start': 0})
    assert response.status_code == 200
    

def test_normal_functionality2(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})  
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"})
    assert response.status_code == 200 
    assert is_valid_dictionary_output(response.json(), {'message_id': int})
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_2, 'channel_id': channel_id, 'message': "Hello World2"})
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {'message_id': int})

def test_check_accessibility_of_messages_across_channels(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_id2 = requests.post(CREATE_URL, json={
                               'token': user_token_2, 'name': 'My Channel2!', 'is_public': True}).json()['channel_id'] 
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Hello World"})
    assert response.status_code == 200 
    assert is_valid_dictionary_output(response.json(), {'message_id': int})
    response = requests.get(CHANNEL_MESSAGES_URL, params={'token': user_token_2,
                                                              'channel_id': channel_id2, 'start': 0})
    assert response.status_code == 200
    # check that channel_id2 has no messages within it
    assert response.json() == {'messages': [], 'start': 0, 'end': -1}

def test_invalid_message(clear_store, create_user):
    # message invalid when length of message is < 1 or > 1000 characters
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': ""})
    assert response.status_code == 400

def test_user_not_part_of_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_2, 'channel_id': channel_id, 'message': "Hello World"})
    assert response.status_code == 403

def test_channel_not_valid(clear_store, create_user):
    user_token_1 = create_user['token']
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': "100", 'message': "Hello World"})
    assert response.status_code == 400
