import pytest
import requests

from src.auth import auth_register_v2
from src.channel import channel_messages_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = '5000'
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"
CHANNEL_MESSAGES_URL = f"{BASE_URL}/channel/messages/v2"

@pytest.fixture
def clear_store():
    clear_v1()
    
@pytest.fixture
def create_user():
    user_token_1 = auth_register_v2("z432324@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_token_1

@pytest.fixture
def create_user2():
    user_token_2 = auth_register_v2("z432325@unsw.edu.au", "password1", "Name1", "Lastname1")['auth_user_id']
    return  user_token_2 

# def test_invalid_channel_id(clear_store, create_user):
#     user_token_1 = create_user
#     with pytest.raises(InputError):
#         channel_messages_v1(user_token_1, 1, 0)

# def test_user_not_in_channel(clear_store, create_user, create_user2):
#     user_token_1 = create_user
#       user_token_2 = create_user2
#     channel_id = channels_create_v1(user_token_1, 'test', True)
#     with pytest.raises(AccessError):
#         channel_messages_v1   user_token_2, channel_id['channel_id'], 0)

# def test_channel_messages_with_no_messages(clear_store, create_user):
#     user_token_1 = create_user
#     channel_id = channels_create_v1(user_token_1, 'test', True)
#     expected_output = { 'messages': [], 'start': 0, 'end': -1 }
#     assert channel_messages_v1(user_token_1, channel_id['channel_id'], 0) == expected_output

# def test_channel_messages_start_exceeds(clear_store, create_user):
#      user_token_1 = create_user
#      channel_id = channels_create_v1(user_token_1, 'test', True)['channel_id']

#      current = 0
#      messages = channel_messages_v1(user_token_1, channel_id, current)
#      # Spew through the messages until we reach the end
#      while messages['end'] != -1:
#          current += 50
#          messages = channel_messages_v1(user_token_1, channel_id, current)
    
#      with pytest.raises(InputError):
#         channel_messages_v1(user_token_1, channel_id, current+100)


# def test_invalid_auth_id(clear_store, create_user):
#     user_token_1 = create_user
#     fake_id = user_token_1 + 1
#     channel_id = channels_create_v1(user_token_1, "Cool", True)['channel_id']
#     with pytest.raises(AccessError):
#         channel_messages_v1(fake_id, channel_id, 0)


def test_invalid_channel_id(clear_store, create_user):
    user_token_1 = create_user
    params = {'user_token': user_token_1, 'channel_id': 1, 'start': 0}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    assert response.status_code != 200

def test_user_not_in_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user
    user_token_2 = create_user2
    channel_id = channels_create_v2(user_token_1, 'test', True)['channel_id']
    params = {'user_token': user_token_2, 'channel_id': channel_id, 'start': 0}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    assert response.status_code != 200

def test_channel_messages_with_no_messages(clear_store, create_user):
    user_token_1 = create_user
    channel_id = channels_create_v2(user_token_1, 'test', True)['channel_id']
    params = {'user_token': user_token_1, 'channel_id': channel_id, 'start': 0}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    expected_output = { 'messages': [], 'start': 0, 'end': -1 }
    assert response.json() == expected_output
    assert response.status_code == 200

def test_channel_messages_start_exceeds(clear_store, create_user):
    user_token_1 = create_user
    channel_id = channels_create_v2(user_token_1, 'test', True)['channel_id']
    current = 0
    params = {'user_token': user_token_1, 'channel_id': channel_id, 'start': current}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    # Spew through the messages until we reach the end
    while response.json(['end']) != -1:
        current += 50
        params = {'user_token': user_token_1, 'channel_id': channel_id, 'start': current}
        response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    
    params = {'user_token': user_token_1, 'channel_id': channel_id, 'start': current + 100}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    assert response.status_code != 200

def test_invalid_auth_id(clear_store, create_user):
    user_token_1 = create_user
    fake_id = user_token_1 + 1
    channel_id = channels_create_v2(user_token_1, "Cool", True)['channel_id']
    params = {'user_token': fake_id, 'channel_id': channel_id, 'start': 0}
    response = requests.get(CHANNEL_MESSAGES_URL, params = params)
    assert response.status_code != 200
