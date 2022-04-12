from src.config import url
import pytest
import requests
import src.other as other


@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au",
                  'password': "badpassword123", 'name_first': "Ji", 'name_last': "Sun"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password",
                  'name_first': "Jane", 'name_last': "Gyuri"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


def test_basic_stats(clear_store, create_user):
    user = create_user
    response = requests.get(other.USER_STATS_URL, params = {'token': user['token']})
    assert response.status_code == 200
    assert response.json()['involvement_rate'] == 0
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json = {'token': user['token'], 'name': 'Happy', 'is_public': True})
    response = requests.get(other.USER_STATS_URL, params = {'token': user['token']})
    assert response.json()['involvement_rate'] == 1
    channels_join = response.json()['channels_joined']
    assert channels_join[0]['channels_joined'] == 0
    assert channels_join[1]['channels_joined'] == 1
    assert channels_join[0]['time'] < channels_join[1]['time']

def test_multi_user_stats(clear_store, create_user, create_user2):
    user1 = create_user
    user2 = create_user2
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json = {'token': user1['token'], 'name': 'Happy', 'is_public': True}).json()['channel_id']
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user1['token'], 'message': 'hey', 'channel_id': channel_id})
    requests.post(other.CHANNEL_JOIN_URL, json = {'token': user2['token'], 'channel_id': channel_id})
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user1['token'], 'message': 'hey', 'channel_id': channel_id})
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user2['token'], 'message': 'hey back', 'channel_id': channel_id})
    response1 = requests.get(other.USER_STATS_URL, params = {'token': user1['token']})
    response2 = requests.get(other.USER_STATS_URL, params = {'token': user2['token']})
    assert response1.json()['involvement_rate'] == 3/4
    assert response2.json()['involvement_rate'] == 1/2

def test_deprecating_stats(clear_store, create_user, create_user2):
    user1 = create_user
    user2 = create_user2
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json = {'token': user1['token'], 'name': 'Happy', 'is_public': True}).json()['channel_id']
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user1['token'], 'message': 'hey', 'channel_id': channel_id})
    requests.post(other.CHANNEL_JOIN_URL, json = {'token': user2['token'], 'channel_id': channel_id})
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user1['token'], 'message': 'hey', 'channel_id': channel_id})
    requests.post(other.MESSAGE_SEND_URL, json = {'token': user2['token'], 'message': 'hey back', 'channel_id': channel_id})
    requests.post(other.CHANNEL_LEAVE_URL, json = {'token': user2['token'], 'channel_id': channel_id})
    response2 = requests.get(other.USER_STATS_URL, params = {'token': user2['token']})
    assert response2.json()['involvement_rate'] == 1/4
