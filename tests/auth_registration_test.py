import pytest
import requests
from src.other import clear_v1, is_valid_dictionary_output
from src.config import port, url


REGISTER_URL = f"{url}/auth/register/v2"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

def test_auth_register_v2(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {'token': str, 'auth_user_id': int})


def test_auth_register_v2_error_email_not_valid(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"tsgyd", "password":"34rd^hds)", "name_first": "Johnny", "name_last":"Smith"})
    assert response.status_code != 200

def test_auth_register_v2_error_password_short(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"pa33", "name_first":"Marc", "name_last":"Chee"})
    assert response.status_code != 200

def test_auth_register_v2_error_email_used(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"thi3isn0t@pa33wor&", "name_first":"Steve", "name_last":"Jobs"})
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {"token": str, "auth_user_id": int})
    response2 = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"newpassword", "name_first":"Steve", "name_last":"Wozniak"})
    assert response2.status_code != 200


def test_auth_register_v2_error_first_name_short(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"longpassword", "name_first":"", "name_last":"Li"})
    assert response.status_code != 200

def test_auth_register_v2_error_first_name_long(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"longpassword", "name_first":"THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY", "name_last":"Li"})
    assert response.status_code != 200
        

def test_auth_register_v2_error_last_name_short(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"goodpass", "name_first":"Simon", "name_last":""})
    assert response.status_code != 200


def test_auth_register_v1_error_last_name_long(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"goodpass", "name_first":"Simon", "name_last":"THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY"})
    assert response.status_code != 200
