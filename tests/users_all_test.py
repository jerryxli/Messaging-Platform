import requests
import pytest
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"
USERS_ALL_URL = f"{url}/users/all/v1"
REMOVE_URL = f"{url}admin/user/remove/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au",
                  'password': "badpassword123", 'name_first': "Ji", 'name_last': "Sun"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password",
                  'name_first': "Jane", 'name_last': "Gyuri"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


# Users All returns {'users': [{u_id, email, name_first, name_last, handle}]}

# No users registered
def test_one_user(clear_store, create_user):
    user_token = create_user['token']
    user_id = create_user['auth_user_id']
    response = requests.get(USERS_ALL_URL, params = {'token': user_token})
    profile_response = requests.get(PROFILE_URL, params = {"u_id": user_id, "token": user_token})
    assert profile_response.json() == {"u_id": user_id, 'email': "z432324@unsw.edu.au", 'name_first': "Ji", 'name_last': "Sun", 'handle_str': "jisun"}
    assert response.json()['users'] == [profile_response.json()]
    assert response.status_code == 200

# Test for multiple users
def test_multiple_users(clear_store, create_user, create_user2):
    user_token = create_user['token']
    user_token2 = create_user2['token']
    user_id = create_user['auth_user_id']
    user_id2 = create_user2['auth_user_id']
    response = requests.get(USERS_ALL_URL, params = {'token': user_token})
    profile_response1 = requests.get(PROFILE_URL, params = {"u_id": user_id, "token": user_token})
    profile_response2 = requests.get(PROFILE_URL, params = {"u_id": user_id2, "token": user_token2})
    assert [profile_response1.json(), profile_response2.json()] == [   {"u_id": user_id, 'email': "z432324@unsw.edu.au", 'name_first': "Ji", 'name_last': "Sun", 'handle_str': "jisun"},
                                                                       {"u_id": user_id2, 'email': "z54626@unsw.edu.au", 'name_first': "Jane", 'name_last': "Gyuri", 'handle_str': "janegyuri"}
                                                                   ]
    assert response.json()['users'] == [profile_response1.json(), profile_response2.json()]
    assert response.status_code == 200
    requests.delete(REMOVE_URL, json = {'token': user_token, 'u_id': user_id2})
    response = requests.get(USERS_ALL_URL, params = {'token': user_token})
    assert response.json() == {'users': [{"u_id": user_id, 'email': "z432324@unsw.edu.au", 'name_first': "Ji", 'name_last': "Sun", 'handle_str': "jisun"}]}
    

# Test for invalid token
def test_invalid_token(clear_store, create_user):
    user_token = create_user['token']
    requests.post(f"{url}/auth/logout/v1", json={"token": user_token})
    response = requests.get(USERS_ALL_URL, params = {"token": user_token})
    assert response.status_code == 403
