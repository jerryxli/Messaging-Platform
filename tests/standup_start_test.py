from src.config import url
import requests
import pytest
import datetime
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z4323234@unsw.edu.au", 'password': "Password1", 'name_first': "Name1", 'name_last': "LastName1"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z546326@unsw.edu.au", 'password': "Password2", 'name_first': "Name2", 'name_last': "LastName2"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info

def test_success_start(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(other.STANDUP_START_URL, json={'token': user_token, 'channel_id': channel_id, 'length': 30})
    time_start = datetime.now()
    time_finish = time_start + datetime.timedelta(seconds = 30)
    
    assert response.status_code == 200

    response_data = response.json()
    assert response_data == datetime.timestamp(time_finish)


def test_negative_length(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(other.STANDUP_START_URL, json={'token': user_token, 'channel_id': channel_id, 'length': -30})
    assert response.status_code == 400

def test_standup_already_running(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response1 = requests.post(other.STANDUP_START_URL, json={'token': user_token, 'channel_id': channel_id, 'length': 30})
    assert response1.status_code == 200

    response2 = requests.post(other.STANDUP_START_URL, json={'token': user_token, 'channel_id': channel_id, 'length': 30})
    assert response2.status_code == 400
    
def test_invalid_channel(clear_store, create_user):
    user_token = create_user['token']
    response = requests.post(other.STANDUP_START_URL, json={'token': user_token, 'channel_id': None, 'length': 30})
    assert response.status_code == 400

def test_unauthorised_member(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={'token': user_token, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response1 = requests.post(other.STANDUP_START_URL, json={'token': user_token_2, 'channel_id': channel_id, 'length': 30})
    assert response1.status_code == 403
    