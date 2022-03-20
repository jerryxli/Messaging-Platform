from src.auth import auth_register_v1
from src.error import AccessError
from src.config import port, url
from src.other import clear_v1
import requests
import pytest

LIST_URL = f"{url}/channels/list/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"

@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Chocolate"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user3():
    user_input = {'email': "z536601@unsw.edu.au", 'password': "1243Bops", 'name_first': "Mars", 'name_last': "Bars"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

# When channels_list_v2 is called, it should return the channel name and channel id.
# In the format: {'channels': {'channel_id': ' ', 'name': ' '}}

# Test for when the user has no channels
def test_no_channels(clear_store, create_user):
    user_token = create_user['token']
    response = requests.get(LIST_URL, params = user_token)
    expected_outcome = { 'channels': [] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when the user has created one channel
def test_one_channel(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'My Channel!', 'is_public': True}).json('channel_id')
    response = requests.get(LIST_URL, params = user_token)
    expected_outcome = { 'channels': [{'channel_id': channel_id, 'name': 'My Channel!'}] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when the user has multiple channels
def test_multiple_channels(clear_store, create_user):
    user_token = create_user['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Cool Channel', 'is_public': True}).json('channel_id')
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'ok channel', 'is_public': False}).json('channel_id')
    channel_id_3 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'BAD CHANNEL', 'is_public': True}).json('channel_id')
    response = requests.get(LIST_URL, params = user_token)
    expected_outcome = { 'channels': [{'channel_id': channel_id_1, 'name': 'Cool Channel'}, {'channel_id': channel_id_2, 'name': 'ok channel'}, {'channel_id': channel_id_3, 'name': 'BAD CHANNEL'}] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when multiple users have created channels
def test_multiple_users(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']

    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'Hangout', 'is_public': True}).json('channel_id')
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'kitchen', 'is_public': True}).json('channel_id')
    channel_id_3 = requests.post(CREATE_URL, json = {'token': user_token_3, 'name': 'LOUNGE', 'is_public': True}).json('channel_id')
    response_1 = requests.get(LIST_URL, params = user_token_1)
    assert response_1.json() == { 'channels': [{'channel_id': channel_id_1, 'name': 'Hangout'}] }
    assert response_1.status_code == 200

    response_2 = requests.get(LIST_URL, params = user_token_2)
    assert response_2.json() == { 'channels': [{'channel_id': channel_id_2, 'name': 'kitchen'}] }
    assert response_2.status_code == 200

    response_3 = requests.get(LIST_URL, params = user_token_3)
    assert response_3.json() == { 'channels': [{'channel_id': channel_id_3, 'name': 'LOUNGE'}] }
    assert response_3.status_code == 200


# Test for when the token is invalid
def test_invalid_user_token(clear_store, create_user):
    # Since we are only creating one user and each id is unique, then user + 1 must be fake
    fake_user = create_user['token'] + 1
    response = response.get(LIST_URL, params = fake_user)
    assert response.status_code == 403
