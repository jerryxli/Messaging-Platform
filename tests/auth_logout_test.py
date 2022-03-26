import pytest
import requests
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"
LOGOUT_URL = f"{url}/auth/logout/v1"
LOGIN_URL = f"{url}/auth/login/v2"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


def test_logout_success(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    logout_request = requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request.status_code == 200
    assert logout_request.json() == {}
    profile_repsonse = requests.get(PROFILE_URL, json={"token": response.json()['token']}, params = {"u_id": response.json()['auth_user_id']})
    assert profile_repsonse.status_code == 403


def test_logout_invalid_token(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    logout_request_1 = requests.post(LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request_1.status_code == 403

def test_logout_multiple_sessions(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    token_0 = response.json()['token']
    u_id = response.json()['auth_user_id']
    login_response = requests.post(LOGIN_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong"})
    token_1 = login_response.json()['token']
    requests.post(LOGOUT_URL, json={"token": token_0})
    profile_repsonse = requests.get(PROFILE_URL, params={"u_id": u_id}, json={"token": token_1})
    assert profile_repsonse.status_code == 200
    profile_repsonse_1 = requests.get(PROFILE_URL, params={"u_id": u_id}, json = {"token": token_0})
    assert profile_repsonse_1.status_code == 403