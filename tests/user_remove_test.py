from src.auth import GLOBAL_PERMISSION_USER
from src.channel import GLOBAL_PERMISSION_OWNER
from src.error import InputError, AccessError
from src.other import clear_v1, is_valid_dictionary_output
from src.config import port, url
from src.user import user_remove_v1
import pytest
import requests

REGISTER_URL = f"{url}/auth/register/v2"
LOGIN_URL = f"{url}/auth/login/v2"
REMOVE_URL = f"{url}admin/user/remove/v1"
PROFILE_URL = f"{url}/user/profile/v1"

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
    response = requests.get(PROFILE_URL, json = {'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert response.status_code == 200
    assert response.json() == {"u_id": user_2['auth_user_id'], "email":"z12345@unsw.edu.au", "name_first": "FirstName", "name_last": "LastName", 'handle_str': 'firstnamelastname'}
    response = requests.delete(REMOVE_URL, json = {'token': user_1['token']})
    assert response.status_code == 200
    response = requests.get(PROFILE_URL, json = {'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert response.json() == {"u_id": user_2['auth_user_id'], "name_first": "Remove", "name_last": "user", "handle_str": ""}

