from src.config import url
import requests
import pytest
from src.other import is_valid_dictionary_output

REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
DM_CREATE_URL = f"{url}/dm/create/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Chocolate"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

@pytest.fixture
def create_user3():
    user_input = {'email': "z536601@unsw.edu.au", 'password': "1243Bops", 'name_first': "Mars", 'name_last': "Bars"}
    request_data = requests.post(REGISTER_URL, json = user_input)
    user_info = request_data.json()
    return user_info

# Dm Create creates a dm and returns a dm_id

# Test successful case -> RETURN DM_ID 
def test_success_create(clear_store, create_user, create_user2, create_user3): 
    user_token_1 = create_user['token']
    user_id_2 = create_user2['auth_user_id']
    user_id_3 = create_user3['auth_user_id']
    response = requests.post(DM_CREATE_URL, json = {'token': user_token_1, 'u_ids': [user_id_2, user_id_3]})
    assert response.json() == {'dm_id': 0} # WHITE BOX JUST TO TEST FOR NOW
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {'dm_id': int})    

# Test empty list of u_ids -> RETURN DM_ID
def test_empty_list(clear_store, create_user):
    user_token_1 = create_user['token']
    response = requests.post(DM_CREATE_URL, json = {'token': user_token_1, 'u_ids': []})
    assert response.json() == {'dm_id': 0} # WHITE BOX JUST TO TEST FOR NOW
    assert response.status_code == 200
    assert is_valid_dictionary_output(response.json(), {'dm_id': int})    

# Test Invalid token -> ACCESS ERROR
def test_invalid_token(clear_store, create_user):
    user_token = create_user['token']
    requests.post(LOGOUT_URL, json = {'token': user_token})
    response = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': []})
    assert response.status_code == 403

# Test invalid u_id -> INPUT ERROR
def test_invalid_u_id(clear_store, create_user):
    user_token = create_user['token']
    response = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [12]})
    assert response.status_code == 400

# Test duplicate u_id -> INPUT ERROR
def test_duplicate_u_id(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_id_2 = create_user2['auth_user_id']
    response = requests.post(DM_CREATE_URL, json = {'token': user_token, 'u_ids': [user_id_2, user_id_2]})
    assert response.status_code == 400


