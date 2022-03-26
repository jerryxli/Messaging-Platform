from src.channels import channels_create_v1 
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from tests.channels_list_test import LIST_URL
from .helper_functions import is_valid_dictionary_output
from src.config import url
import pytest
import requests

CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
DETAILS_URL = f"{url}/channel/details/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Chocolate"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

def test_add_public_channel(clear_store, create_user, create_user2):
    user1 = create_user
    channel_id = requests.post(CREATE_URL, json = {'token': user1['token'], 'name': 'my house', 'is_public': True}).json()['channel_id']
    response = requests.get(LIST_URL, json = {'token': user1['token']})
    assert response.json() == { 'channels': [{'channel_id': channel_id, 'name': 'my house'}]}
    response = requests.get(DETAILS_URL, json = {'token': user1['token'], 'channel_id': channel_id})


def test_add_private_channel(clear_store, create_user):
    user1 = create_user
    channel_id = requests.post(CREATE_URL, json = {'token': user1['token'], 'name': 'my house', 'is_public': False}).json()['channel_id']
    response = requests.get(LIST_URL, json = {'token': user1['token']})
    assert response.json() == { 'channels': [{'channel_id': channel_id, 'name': 'my house'}]}
    

def test_null_name(clear_store, create_user):
    user1 = create_user
    response = requests.post(CREATE_URL, json = {'token': user1['token'], 'name': '', 'is_public': True})
    assert response.status_code == 400
    

def test_long_name(clear_store, create_user):
    user1 = create_user
    response = requests.post(CREATE_URL, json = {'token': user1['token'], 'name': 'sadoiasjdoiasjdoaisdjaoisdjaoisdjaoisjdadsjgfoiasjfgoiasjdfoiajsdofiajsdoifjaosdifjaoisdjf', 'is_public': True})
    assert response.status_code == 400

def test_invalid_JWT(clear_store, create_user):
    user1 = create_user
    requests.post(LOGOUT_URL, json = {'token': user1['token']})
    response = requests.post(CREATE_URL, json = {'token': user1['token'], 'name': 'hello', 'is_public': True})
    assert response.status_code == 403


