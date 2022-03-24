from src.config import url
import pytest
import requests

REGISTER_URL = f"{url}/auth/register/v2"
DM_CREATE_URL = f"{url}/dm/create/v1"
DM_LIST_URL = f"{url}/dm/list/v1"
DM_REMOVE_URL = f"{url}/dm/remove/v1"
DM_LEAVE_URL = f"{url}/dm/leave/v1"

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

# check_dm_id_is_removed(token, dm_id):


def_test_remove_dm(clear_store, create_user,create_user2):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']

    dm_id = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]}).json()['dm_id']

    response = requests.delete(DM_REMOVE_URL, json = {'token': user_token, 'dm_id': dm_id})
    assert response.status_code == 200

# already removed or not existing in the first place
def_test_invalid_dm_id(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']

    dm_id = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]}).json()['dm_id']

    response = requests.delete(DM_REMOVE_URL, json = {'token': user_token, 'dm_id': dm_id})
    assert response.status_code == 200
    response = requests.delete(DM_REMOVE_URL, json = {'token': user_token, 'dm_id': dm_id})
    assert response.status_code == 400

# member in dm that is not creator tries to remove dm
def_test_not_dm_creator(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']
    user_token_2 = create_user2['token']

    dm_id = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]}).json()['dm_id']

    response = requests.delete(DM_REMOVE_URL, json = {'token': user_token_2, 'dm_id': dm_id})
    assert response.status_code == 403

def_test_auth_user_no_longer_in_dm(clear_store, create_user):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']

    dm_id = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2]}).json()['dm_id']
    requests.post(DM_LEAVE_URL, json = {'token': user_token, 'dm_id': dm_id})

    response = requests.delete(DM_REMOVE_URL, json = {'token': user_token_2, 'dm_id': dm_id})
    assert response.status_code == 403