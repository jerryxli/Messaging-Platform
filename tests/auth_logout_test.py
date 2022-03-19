import pytest
import requests
from src.error import InputError, AccessError
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"
LOGOUT_URL = f"{url}/auth/logout/v1"

@pytest.fixtures
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


def test_logout_success():
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    logout_request = requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request.status_code == 200
    assert logout_request.json() == {}
    profile_repsonse = requests.get(PROFILE_URL, params={"token": response.json()['token'], "u_id": response.json()['token']})
    assert profile_repsonse.status_code == 403


def test_logout_invalid_token():
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    logout_request_1 = requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request_1.status_code == 403