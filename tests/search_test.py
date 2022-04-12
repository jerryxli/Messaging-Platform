from src.config import url
from time import time
import pytest
import requests
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user1():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Fix"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def long_string():
    string = ''
    for i in range(1,1000):
        string += str(i)
    return string

def test_message_contains_query(clear_store, create_user1):
    user_token = create_user1['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(other.MESSAGE_SEND_URL, json={'token': user_token, 'channel_id': channel_id, 'message': "Query word hello"}).json()['message_id']
    channel_messages = requests.get(other.CHANNEL_MESSAGES_URL, params={'token': user_token, 'channel_id': channel_id, 'start': 0}).json()
    response = requests.get(other.SEARCH_URL, params={'token': user_token, 'query_str': "hello"})
    expected_output = channel_messages['messages']
    assert response.json()['messages'] == expected_output
    assert response.status_code == 200

def test_message_do_not_contain_query(clear_store, create_user1):
    user_token = create_user1['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(other.MESSAGE_SEND_URL, json={'token': user_token, 'channel_id': channel_id, 'message': "hello"})
    response = requests.get(other.SEARCH_URL, params={'token': user_token, 'query_str': "word"})
    expected_output = {'messages': []}
    assert response.json() == expected_output
    assert response.status_code == 200

def test_query_too_long(clear_store, create_user1, long_string):
    user_token = create_user1['token']
    create_user1['auth_user_id']
    requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    response = requests.get(other.SEARCH_URL, params={'token': user_token, 'query_str': long_string})
    assert response.status_code == 400

def test_invalid_user(clear_store, create_user1):
    user_token = create_user1['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(other.MESSAGE_SEND_URL, json={'token': user_token, 'channel_id': channel_id, 'message': "Hello"})
    requests.post(other.LOGOUT_URL, json={'token': user_token})
    request_data = requests.get(other.SEARCH_URL, params={'token': user_token, 'query_str': "Hello"})
    assert request_data.status_code == 403
