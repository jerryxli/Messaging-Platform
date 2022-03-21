import requests
import pytest
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

def test_normal_profile(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    user_0_token = response.json()['token']
    user_0_id = response.json()['auth_user_id']
    profile_repsonse = requests.get(PROFILE_URL, params={"token": user_0_token, "u_id": user_0_id})
    assert profile_repsonse.json() == {"u_id": user_0_id, "name_first": "Jake", "name_last": "Renzella", "handle_str": "jakerenzella"}

def test_invalid_token(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    user_0_token = response.json()['token']
    user_0_id = response.json()['auth_user_id']
    requests.post(f"{url}/auth/logout/v1", json={"token": user_0_token})
    profile_repsonse = requests.get(PROFILE_URL, params={"token": user_0_token, "u_id": user_0_id})
    assert profile_repsonse.status_code == 403    

def test_invalid_user_id(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    user_0_token = response.json()['token']
    user_0_id = response.json()['auth_user_id']
    profile_repsonse = requests.get(PROFILE_URL, params={"token": user_0_token, "u_id": user_0_id + 1})
    assert profile_repsonse.status_code == 400