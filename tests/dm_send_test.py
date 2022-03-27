from src.config import url
import requests
import pytest

CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
DM_CREATE_URL = f"{url}/dm/create/v1"
DM_SEND_URL = f"{url}/message/senddm/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json = {})
    
@pytest.fixture
def register_user_1():
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"}).json()
    return response

@pytest.fixture
def register_user_2():
    response = requests.post(REGISTER_URL, json = {"email":"z12345@unsw.edu.au", "password": "epicpassword", "name_first": "FirstName", "name_last": "LastName"}).json()
    return response

def test_basic_success(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json = {"token": user_1['token'], "u_ids": [user_2['auth_user_id']]}).json()['dm_id']
    response = requests.post(DM_SEND_URL, json = {'token': user_1['token'], "dm_id": dm_id, 'message': 'HELLO THERE'})
    assert response.status_code == 200
    assert response.json()['message_id'] == 0

def test_short_message(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json = {"token": user_1['token'], "u_ids": [user_2['auth_user_id']]}).json()['dm_id']
    response = requests.post(DM_SEND_URL, json = {'token': user_1['token'], "dm_id": dm_id, 'message': ''})
    assert response.status_code == 400

def test_long_message(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json = {"token": user_1['token'], "u_ids": [user_2['auth_user_id']]}).json()['dm_id']
    response = requests.post(DM_SEND_URL, json = {'token': user_1['token'], "dm_id": dm_id, 'message': '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'})
    assert response.status_code == 400

def test_invalid_dm_id(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json = {"token": user_1['token'], "u_ids": [user_2['auth_user_id']]}).json()['dm_id']
    response = requests.post(DM_SEND_URL, json = {'token': user_1['token'], "dm_id": dm_id + 400, 'message': '1234567890'})
    assert response.status_code == 400

def test_user_not_in_channel(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json = {"token": user_1['token'], "u_ids": []}).json()['dm_id']
    response = requests.post(DM_SEND_URL, json = {'token': user_2['token'], "dm_id": dm_id, 'message': '1234567890'})
    assert response.status_code == 403
    
    