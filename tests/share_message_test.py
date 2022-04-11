from ssl import CHANNEL_BINDING_TYPES
import requests
import pytest
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})
    
@pytest.fixture
def register_user_1():
    response = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"}).json()
    return response

@pytest.fixture
def register_user_2():
    response = requests.post(other.REGISTER_URL, json={"email":"z12345@unsw.edu.au", "password": "epicpassword", "name_first": "FirstName", "name_last": "LastName"}).json()
    return response

def test_basic_share_from_channel_to_dm(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json = {"token": user_1['token'], 'name': 'apples', 'is_public': True}).json()['channel_id']
    dm_id = requests.post(other.DM_CREATE_URL, json = {'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]}).json()['dm_id']
    message_id = requests.post(other.MESSAGE_SEND_URL, json = {'token': user_1['token'], 'message': 'hey', 'channel_id': channel_id}).json()['message_id']
    response = requests.post(other.MESSAGE_SHARE_URL, json = {'token': user_1['token'], 'og_message_id': message_id, 'message': 'double hey', 'channel_id': -1, 'dm_id': dm_id})
    assert response.status_code == 200
    response = requests.get(other.DM_MESSAGES_URL, params = {'dm_id': dm_id, 'token': user_1['token'], 'start': 0})
    expected_output = "> hey\ndouble hey"
    assert response.json()['messages'][0]['message'] == expected_output
    
def test_basic_share_from_dm_to_channel(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json = {"token": user_1['token'], 'name': 'apples', 'is_public': True}).json()['channel_id']
    dm_id = requests.post(other.DM_CREATE_URL, json = {'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]}).json()['dm_id']
    message_id = requests.post(other.MESSAGE_SENDDM_URL, json = {'token': user_1['token'], 'message': 'hey', 'dm_id': dm_id}).json()['message_id']
    response = requests.post(other.MESSAGE_SHARE_URL, json = {'token': user_1['token'], 'og_message_id': message_id, 'message': 'double hey', 'channel_id': channel_id, 'dm_id': -1})
    assert response.status_code == 200
    response = requests.get(other.CHANNEL_MESSAGES_URL, params = {'channel_id': channel_id, 'token': user_1['token'], 'start': 0})
    expected_output = "> hey\ndouble hey"
    assert response.json()['messages'][0]['message'] == expected_output