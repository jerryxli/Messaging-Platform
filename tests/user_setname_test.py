import pytest
import requests
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"
LOGOUT_URL = f"{url}/auth/logout/v1"
SETNAME_URL = f"{url}/user/profile/setname/v1"


@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

def test_set_name_success(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    user_id = registration_request.json()['auth_user_id']
    token = registration_request.json()['token']
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "John", "name_last": "Smith"})
    assert setname_request.status_code == 200
    assert setname_request.json() == {}
    new_profile = requests.get(PROFILE_URL, params={"u_id": user_id, "token": token})
    assert new_profile.json()['user'] == {"u_id": user_id, "email": "z55555@unsw.edu.au", "name_first": "John", "name_last": "Smith", "handle_str": "jakerenzella"}


def test_invalid_token(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token = registration_request.json()['token']
    requests.post(LOGOUT_URL, json={"token": token})
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "John", "name_last": "Smith"})
    assert setname_request.status_code == 403

def test_short_first_name(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token = registration_request.json()['token']
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "", "name_last": "Smith"})
    assert setname_request.status_code == 400

def test_short_last_name(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token = registration_request.json()['token']
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "John", "name_last": ""})
    assert setname_request.status_code == 400

def test_long_first_name(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token = registration_request.json()['token']
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "THISISAVERYLONGNAMEWHICHISCERTAINLYOUTOFTHERELEVANTBOUNDS", "name_last": "Smith"})
    assert setname_request.status_code == 400

def test_long_last_name(clear_store):
    registration_request = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token = registration_request.json()['token']
    setname_request = requests.put(SETNAME_URL, json={"token": token, "name_first": "John", "name_last": "THISISAVERYLONGNAMEWHICHISCERTAINLYOUTOFTHERELEVANTBOUNDS"})
    assert setname_request.status_code == 400