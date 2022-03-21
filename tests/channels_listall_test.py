from src.config import url

import requests
import pytest
import jwt

LISTALL_URL = f"{url}/channels/listall/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
JWT_SECRET = "COMP1531_H13A_CAMEL"
LOGOUT_URL = f"{url}/auth/logout/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z2537530@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Chocolate"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z934183@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

# Access error when auth_user_id is invalid
def test_listall_v2_auth_user_id_invalid(clear_store):
    response = requests.get(LISTALL_URL, params = {})
    response_data = response.json()
    assert response.status_code == 403
    assert response_data == None

# Test for when there are no channels
def test_listall_v2_no_channels(clear_store, create_user):
    user_token = create_user['token']
    response = requests.get(LISTALL_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {'channels': []} 

# Test for when there is only one public channel
def test_listall_v2_one_public(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel1', 'is_public': True}).json()['channel_id']
    
    response = requests.get(LISTALL_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {'channels': [{'channel_id': channel_id, 'name': 'Channel1'}]}

def test_listall_v2_mul_privacy(clear_v1, create_user):
    # create all the channels
    user_token = create_user['token']
    channel_id1 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel1', 'is_public': True}).json()['channel_id']
    channel_id2 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel2', 'is_public': False}).json()['channel_id']
    channel_id3 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel3', 'is_public': True}).json()['channel_id']
    channel_id4 = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel4', 'is_public': False}).json()['channel_id']

    
    response = requests.get(LISTALL_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200

    expected = {'channels': [{'channel_id': channel_id1, 'name': 'Channel1'}, {'channel_id': channel_id2, 'name': 'Channel2'}, {'channel_id': channel_id3, 'name': 'Channel3'}, {'channel_id': channel_id4, 'name': 'Channel4'}]}
    assert response_data == expected


#--------- Test for channels user isin't part of -----------#

# Test for public and private channels user isin't part of
def test_listall_v2_not_in_bothprivacy(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']

    channel_id1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'Channel1', 'is_public': True}).json()['channel_id']
    channel_id2 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'Channel2', 'is_public': False}).json()['channel_id']
    channel_id3 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'Channel3', 'is_public': True}).json()['channel_id']
    channel_id4 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'Channel4', 'is_public': False}).json()['channel_id']

    response_1 = requests.get(LISTALL_URL, params = {'token': user_token_1})
    response_data_1 = response_1.json()
    assert response_1.status_code == 200

    expected = {'channels': [{'channel_id': channel_id1, 'name': 'Channel1'}, {'channel_id': channel_id2, 'name': 'Channel2'}, {'channel_id':  channel_id3, 'name': 'Channel3'}, {'channel_id': channel_id4, 'name': 'Channel4'}]}
    assert response_data_1 == expected

    response_2 = requests.get(LISTALL_URL, params = {'token': user_token_2})
    response_data_2 = response_1.json()
    assert response_2.status_code == 200
    assert response_data_2 == expected
  

# Test for when the token is invalid
def test_invalid_user_token(clear_store):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json = {'token': user_token})
    response = requests.get(LISTALL_URL, params = {'token': user_token})
    assert response.status_code == 403




