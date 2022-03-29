from src.config import url
import requests
import pytest
import jwt


DETAILS_URL = f"{url}/channel/details/v2"
JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LEAVE_URL = f"{url}/channel/leave/v1"
LOGOUT_URL = f"{url}/auth/logout/v1"
JWT_SECRET = "COMP1531_H13A_CAMEL"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Chocolate"}
    user_info = requests.post(REGISTER_URL, json=user_input).json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    user_info = requests.post(REGISTER_URL, json=user_input).json()
    return user_info

@pytest.fixture
def create_user3():
    user_input = {'email': "z536601@unsw.edu.au", 'password': "1243Bops", 'name_first': "Mars", 'name_last': "Bars"}
    user_info = requests.post(REGISTER_URL, json=user_input).json()
    return user_info

# The Channel leave function takes in user token and channel id as input
# The function removes the member or owner from the channel

# Tests for when the owner leaves the channel
def test_owner_leaves(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id_1 = requests.post(CREATE_URL, json={'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_id_2 = requests.post(CREATE_URL, json={'token': user_token_2, 'name': 'kitchen', 'is_public': False}).json()['channel_id']
    request_data_1 = requests.post(LEAVE_URL, json={'token': user_token_1, 'channel_id': channel_id_1})
    request_data_2 = requests.post(LEAVE_URL, json={'token': user_token_2, 'channel_id': channel_id_2})
    channel_details_1 = requests.get(DETAILS_URL, params={'channel_id': channel_id_2, 'token': user_token_2})
    channel_details_2 = requests.get(DETAILS_URL, params={'channel_id': channel_id_1, 'token': user_token_1})

    assert request_data_1.json() == {}
    assert request_data_1.status_code == 200
    assert request_data_2.json() == {}
    assert request_data_2.status_code == 200
    # Access Error when trying to get details
    assert channel_details_1.status_code == 403
    assert channel_details_2.status_code == 403 


# Tests for when a member leaves the channel
def test_member_leaves(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    requests.post(JOIN_URL, json={'token': user_token_2, 'channel_id': channel_id})
    request_data_1 = requests.post(LEAVE_URL, json={'token': user_token_2, 'channel_id': channel_id})
    channel_details_1 = requests.get(DETAILS_URL, params={'channel_id': channel_id, 'token': user_token_1})
    channel_details_2 = requests.get(DETAILS_URL, params={'channel_id': channel_id, 'token': user_token_2})
    expected_output_1 = {   'name': 'My Channel!', 
                            'is_public': True,
                            'owner_members': [
                                {
                                    'u_id': create_user['auth_user_id'],
                                    'email': "z432324@unsw.edu.au",
                                    'name_first': "Twix",
                                    'name_last': "Chocolate",
                                    'handle_str': "twixchocolate",
                                }
                            ],
                            'all_members': [
                                {
                                    'u_id': create_user['auth_user_id'],
                                    'email': "z432324@unsw.edu.au",
                                    'name_first': "Twix",
                                    'name_last': "Chocolate",
                                    'handle_str': "twixchocolate",
                                }
                            ],
                        }
    assert channel_details_1.json() == expected_output_1
    assert request_data_1.json() == {}
    assert request_data_1.status_code == 200
    assert channel_details_1.status_code == 200
    assert channel_details_2.status_code == 403

# Test for when a user_token is invalid
def test_invalid_member(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json={'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json={'token': user_token})
    response = requests.post(LEAVE_URL, json={'token': user_token, 'channel_id': channel_id})
    assert response.status_code == 403


# Tests for when the user_id entered is not a member of the channel_id.
def test_unauthorised_user_id(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id_1 = requests.post(CREATE_URL, json={'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_id_2 = requests.post(CREATE_URL, json={'token': user_token_2, 'name': 'kitchen', 'is_public': False}).json()['channel_id']
    request_data_1 = requests.post(LEAVE_URL, json={'token': user_token_2, 'channel_id': channel_id_1})
    request_data_2 = requests.post(LEAVE_URL, json={'token': user_token_3, 'channel_id': channel_id_2})
    assert request_data_1.status_code == 403
    assert request_data_2.status_code == 403


# Tests for when an invalid channel_id is entered.
def test_invalid_channel_id(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = 0
    request_data_1 = requests.post(LEAVE_URL, json={'token': user_token_1, 'channel_id': channel_id})
    request_data_2 = requests.post(LEAVE_URL, json={'token': user_token_2, 'channel_id': channel_id})
    assert request_data_1.status_code == 400
    assert request_data_2.status_code == 400