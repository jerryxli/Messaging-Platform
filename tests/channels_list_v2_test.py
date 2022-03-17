from src.channels import channels_list_v2
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import AccessError
from src.other import clear_v1

import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = '5000'
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_info = auth_register_v2("z432324@unsw.edu.au", "badpassword123", "Twix", "Chocolate")
    return user_info

@pytest.fixture
def create_user2():
    user_info = auth_register_v2("z54626@unsw.edu.au", "Password", "Snickers", "Lickers")
    return user_info

@pytest.fixture
def create_user3():
    user_info = auth_register_v2("z536601@unsw.edu.au", "1243Bops", "Mars", "Bars")
    return user_info

# When channels_list_v2 is called, it should return the channel name and channel id.
# In the format: {'channels': {'channel_id': ' ', 'name': ' '}}

# Test for when the user has no channels
def test_no_channels(clear_store, create_user):
    user_token = create_user['token']
    response = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token)
    expected_outcome = { 'channels': [] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when the user has created one channel
def test_one_channel(clear_store, create_user):
    user_token = create_user['token']
    channel_id = channels_create_v2(user_token, 'My Channel!', True)['channel_id']
    response = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token)
    expected_outcome = { 'channels': [{'channel_id': channel_id, 'name': 'My Channel!'}] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when the user has multiple channels
def test_multiple_channels(clear_store, create_user):
    user_token = create_user['token']
    channel_id_1 = channels_create_v2(user_token, 'Cool Channel', True)['channel_id']
    channel_id_2 = channels_create_v2(user_token, 'ok channel', False)['channel_id']
    channel_id_3 = channels_create_v2(user_token, 'BAD CHANNEL', True)['channel_id']
    response = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token)
    expected_outcome = { 'channels': [{'channel_id': channel_id_1, 'name': 'Cool Channel'}, {'channel_id': channel_id_2, 'name': 'ok channel'}, {'channel_id': channel_id_3, 'name': 'BAD CHANNEL'}] }
    assert response.json() == expected_outcome
    assert response.status_code == 200


# Test for when multiple users have created channels
def test_multiple_users(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']

    channel_id_1 = channels_create_v2(user_token_1, 'Name 1', True)['channel_id']
    channel_id_2 = channels_create_v2(user_token_2, 'Name 2', False)['channel_id']
    channel_id_3 = channels_create_v2(user_token_3, 'Name 3', True)['channel_id']
    response_1 = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token_1)
    assert response_1.json() == { 'channels': [{'channel_id': channel_id_1, 'name': 'Name 1'}] }
    assert response_1.status_code == 200

    response_2 = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token_2)
    assert response_2.json() == { 'channels': [{'channel_id': channel_id_2, 'name': 'Name 2'}] }
    assert response_2.status_code == 200

    response_3 = requests.get(f"{BASE_URL}/channels/list/v2", params = user_token_3)
    assert response_3.json() == { 'channels': [{'channel_id': channel_id_3, 'name': 'Name 3'}] }
    assert response_3.status_code == 200


# Test for when the token is invalid
def test_invalid_user_token(clear_store, create_user):
    # Since we are only creating one user and each id is unique, then user + 1 must be fake
    fake_user = create_user['token'] + 1
    response = response.get(f"{BASE_URL}/channels/list/v2", params = fake_user)
    assert response.status_code != 200
