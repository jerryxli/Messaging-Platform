from src.config import url
import pytest
import requests

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
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_1, 'channel_id': channel_id, 'start': 0})
    # no messages
    assert response.json() == {'messages': [], 'start': 0, 'end': -1}         
    # send a message
    response = requests.post(MESSAGE_SEND_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'message': "Leo loves tests!"})      
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_1, 'channel_id': channel_id, 'start': 0})
    # check if message is there
    assert response.json()['start'] == 0
    assert response.json()['end'] == -1
    assert response.json()['messages'][0]['message'] == "Leo loves tests!"
    assert response.json()['messages'][0]['message_id'] == 0
    assert response.json()['messages'][0]['u_id'] == 0

def test_invalid_channel_id(clear_store, create_user):
    user_token_1 = create_user['token']
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_1, 'channel_id': 1, 'start': 0})
    assert response.status_code == 400


def test_user_not_in_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_2, 'channel_id': channel_id, 'start': 0})
    assert response.status_code == 403


def test_channel_messages_with_no_messages(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_1, 'channel_id': channel_id, 'start': 0})
    expected_output = {'messages': [], 'start': 0, 'end': -1}
    assert response.json() == expected_output
    assert response.status_code == 200


def test_channel_messages_start_exceeds(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    current = 0
    response = requests.get(CHANNEL_MESSAGES_URL, params={'token': user_token_1,
                                                          'channel_id': channel_id, 'start': current})
    # Spew through the messages until we reach the end
    while response.json()['end'] != -1:
        current += 50
        response = requests.get(CHANNEL_MESSAGES_URL, params={'token': user_token_1,
                                                              'channel_id': channel_id, 'start': current})
    response = requests.get(CHANNEL_MESSAGES_URL, params={'token': user_token_1,
                                                          'channel_id': channel_id, 'start': current + 100})
    assert response.status_code == 400


def test_invalid_auth_id(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json={'token': user_token_1})
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'token': user_token_1, 'channel_id': channel_id, 'start': 0})
    assert response.status_code == 403
