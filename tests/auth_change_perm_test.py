from src.auth import GLOBAL_PERMISSION_USER
from src.channel import GLOBAL_PERMISSION_OWNER
from src.error import InputError, AccessError
from src.other import clear_v1, is_valid_dictionary_output
from src.config import port, url
import pytest
import requests

CHANGE_PERM_URL = f"{url}/admin/userpermission/change/v1"
REGISTER_URL = f"{url}/auth/register/v2"
LOGIN_URL = f"{url}/auth/login/v2"

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
    admin = register_user_1
    user = register_user_2
    requests.post(CHANGE_PERM_URL, json={"token": admin['token'], "u_id": user['auth_user_id'], "permission_id": GLOBAL_PERMISSION_OWNER})
    response = requests.post(CHANGE_PERM_URL, json={"token": user['token'], "u_id": admin['auth_user_id'], "permission_id": GLOBAL_PERMISSION_USER})
    assert response.status_code == 200
    
def test_only_one_owner(clear_store, register_user_1):
    admin = register_user_1
    response = requests.post(CHANGE_PERM_URL, json={"token": admin['token'], "u_id": admin['auth_user_id'], "permission_id": GLOBAL_PERMISSION_USER})
    assert response.status_code == 400


def test_invalid_u_id(clear_store, register_user_1, register_user_2):
    admin = register_user_1
    user = register_user_2
    response = requests.post(CHANGE_PERM_URL, json={"token": admin['token'], "u_id": user['auth_user_id'] + 1, "permission_id": GLOBAL_PERMISSION_OWNER})
    assert response.status_code == 400


def test_invalid_permission_id(clear_store, register_user_1, register_user_2):
    admin = register_user_1
    user = register_user_2
    response = requests.post(CHANGE_PERM_URL, json={"token": admin['token'], "u_id": user['auth_user_id'], "permission_id": -1})
    assert response.status_code == 400


def test_same_permission_id(clear_store, register_user_1, register_user_2):
    admin = register_user_1
    user = register_user_2
    response = requests.post(CHANGE_PERM_URL, json={"token": admin['token'], "u_id": user['auth_user_id'], "permission_id": GLOBAL_PERMISSION_USER})
    assert response.status_code == 400


def test_unauthorised_attempt(clear_store, register_user_1, register_user_2):
    user = register_user_2
    response = requests.post(CHANGE_PERM_URL, json={"token": user['token'], "u_id": user['auth_user_id'], "permission_id": GLOBAL_PERMISSION_OWNER})
    assert response.status_code == 403


def test_invalid_jwt(clear_store, register_user_1):
    admin = register_user_1
    response = requests.post(CHANGE_PERM_URL, json={"token": admin['token'] + "1235345", "u_id": admin['auth_user_id'], "permission_id": GLOBAL_PERMISSION_OWNER})
    assert response.status_code == 500
    