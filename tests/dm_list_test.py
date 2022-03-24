from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.auth import auth_register_v1 
from src.error import InputError, AccessError
from src.config import url

import requests
import pytest

CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
DM_CREATE_URL = f"{url}/dm/create/v1"
DM_LIST_URL = f"{url}/dm/list/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z4323234@unsw.edu.au", 'password': "Password1", 'name_first': "Name1", 'name_last': "LastName1"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z546326@unsw.edu.au", 'password': "Password2", 'name_first': "Name2", 'name_last': "LastName2"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user3():
    user_input = {'email': "z5362601@unsw.edu.au", 'password': "Password3", 'name_first': "Name3", 'name_last': "LastName3"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

def test_list_not_in_any_dms(clear_store, create_user):
    user_token = create_user['token']

    response = requests.get(DM_LIST_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {'dms': [] }

def test_list_in_one_dm(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']

    response0 = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]})
    dm_id = response0.json()['dm_id']

    response = requests.get(DM_LIST_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {'dms': [{'dm_id': dm_id, 'name': "name1lastname1, name2lastname2"}] }

def test_list_in_multiple_dm(clear_store, create_user, create_user2, create_user3):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']
    user_id_3 = create_user3['auth_user_id']

    response_data_1 = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]}).json()
    dm_id_1 = response_data_1['dm_id']
    response_data_2 = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2, user_id_3]}).json()
    dm_id_2 = response_data_2['dm_id']

    response = requests.get(DM_LIST_URL, params = {'token': user_token})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {'dms': [{'dm_id': dm_id_1, 'name': "name1lastname1, name2lastname2"}, {'dm_id': dm_id_2, 'name': "name1lastname1, name2lastname2, name3lastname3"}]}

def test_invalid_token(clear_store, create_user):
    user_token = create_user['token']
    requests.post(LOGOUT_URL, json = {'token': user_token})
    response = requests.get(DM_LIST_URL, params = {'token': user_token})
    assert response.status_code == 403
    

