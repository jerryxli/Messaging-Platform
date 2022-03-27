import requests
import pytest
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
SETHANDLE_URL = f"{url}/user/profile/sethandle/v1"
PROFILE_URL = f"{url}/user/profile/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


@pytest.fixture
def register_user_1():
    request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Hayden", "name_last":"Jacobs"})
    return request.json()

@pytest.fixture
def register_user_2():
    request = requests.post(REGISTER_URL, json={"email":"z55556@unsw.edu.au", "password":"passwordlong", "name_first":"Jane", "name_last":"Doe"})
    return request.json()

def test_nomal_success(clear_store, register_user_1):
    user_token = register_user_1['token']
    user_id = register_user_1['auth_user_id']

    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": "iamthebest"})
    assert change_request.status_code == 200
    assert change_request.json() == {}
    profile_repsonse = requests.get(PROFILE_URL, params={"token": user_token, "u_id": user_id})
    print(profile_repsonse.json())
    assert profile_repsonse.json()['handle_str'] == 'iamthebest'

def test_invalid_token(clear_store, register_user_1):
    user_token = register_user_1['token']
    requests.post(f"{url}/auth/logout/v1", json={"token": user_token})
    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": "iamthebest"})
    assert change_request.status_code == 403

def test_handle_short(clear_store, register_user_1):
    user_token = register_user_1['token']
    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": "12"})
    assert change_request.status_code == 400

def test_handle_long(clear_store, register_user_1):
    user_token = register_user_1['token']
    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": "thisisforsurelongerthanthe20charactermaximum"})
    assert change_request.status_code == 400

def test_not_alphanumeric(clear_store, register_user_1):
    user_token = register_user_1['token']
    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": "thisis(*("})
    assert change_request.status_code == 400


def test_handle_in_use(clear_store, register_user_1, register_user_2):
    user_token = register_user_1['token']
    user_2_id = register_user_2['auth_user_id']
    profile_repsonse = requests.get(PROFILE_URL, params={"token": user_token, "u_id": user_2_id})
    user2_handle = profile_repsonse.json()['handle_str']
    change_request = requests.put(SETHANDLE_URL, json={"token": user_token, "handle_str": user2_handle})
    assert change_request.status_code == 400