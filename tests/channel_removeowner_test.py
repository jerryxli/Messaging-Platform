from src.config import url
import requests
import pytest

DETAILS_URL = f"{url}/channel/details/v2"
JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
ADDOWNER_URL = f"{url}/channel/addowner/v1"
REMOVEOWNER_URL = f"{url}/channel/removeowner/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au", 'password': "badpassword123", 'name_first': "Twix", 'name_last': "Fix"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def create_user2():
    user_input = {'email': "z54626@unsw.edu.au", 'password': "Password", 'name_first': "Snickers", 'name_last': "Lickers"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def create_user3():
    user_input = {'email': "z536601@unsw.edu.au", 'password': "1243Bops", 'name_first': "Mars", 'name_last': "Bars"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def create_user4():
    user_input = {'email': "z234019@unsw.edu.au", 'password': "slobknob", 'name_first': "Kit", 'name_last': "Kat"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

# The Channel leave function takes in user token and channel id as input
# The function removes the member or owner from the channel

# Tests for when a channel owner removes an owner
def test_owner_removeowner(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    requests.post(JOIN_URL, json = {'token': user_token_2, 'channel_id': channel_id_1})
    requests.post(ADDOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_1, 'u_id': create_user2['auth_user_id']})
    channel_details_1 = requests.get(DETAILS_URL, params = {'token': user_token_1, 'channel_id': channel_id_1}).json()
    request_data_1 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_1, 'u_id': create_user2['auth_user_id']})
    
    channel_details_2 = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id_1}).json()

    assert request_data_1.json() == {}
    assert request_data_1.status_code == 200

    assert channel_details_1['owner_members'] == [
                                                    {
                                                        'u_id': create_user['auth_user_id'],
                                                        'email': "z432324@unsw.edu.au",
                                                        'name_first': "Twix",
                                                        'name_last': "Fix",
                                                        'handle_str': "twixfix",
                                                    },
                                                    {
                                                        'u_id': create_user2['auth_user_id'],
                                                        'email': "z54626@unsw.edu.au",
                                                        'name_first': "Snickers",
                                                        'name_last': "Lickers",
                                                        'handle_str': "snickerslickers",
                                                    },   
                                                 ]
    assert channel_details_2['owner_members'] == [
                                                    {
                                                        'u_id': create_user['auth_user_id'],
                                                        'email': "z432324@unsw.edu.au",
                                                        'name_first': "Twix",
                                                        'name_last': "Fix",
                                                        'handle_str': "twixfix",
                                                    }   
                                                 ]

# Tests for when a global owner removes an owner
def test_global_owner_remove_themselves(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_id = create_user['auth_user_id']
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'kitchen', 'is_public': True}).json()['channel_id']
    join_request = requests.post(JOIN_URL, json = {'token': user_token_1, 'channel_id': channel_id_2})
    add_request = requests.post(ADDOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_2, 'u_id': user_id})
    response = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_2, 'u_id': user_id})
    channel_details = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id_2}).json()
   
    assert join_request.status_code == 200
    assert add_request.status_code == 200
    assert response.json() == {}
    assert response.status_code == 200
    
    assert channel_details['owner_members'] ==  [
                                                    {
                                                        'u_id': create_user2['auth_user_id'],
                                                        'email': "z54626@unsw.edu.au",
                                                        'name_first': "Snickers",
                                                        'name_last': "Lickers",
                                                        'handle_str': "snickerslickers",
                                                    }  
                                                ]

# Test for when a global_owner removes an owner
def test_global_owner_remove_owner(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(JOIN_URL, json = {'token': user_token_3, 'channel_id': channel_id_2})
    requests.post(ADDOWNER_URL, json = {'token': user_token_2, 'channel_id': channel_id_2, 'u_id': create_user3['auth_user_id']})
    response = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_2, 'u_id': create_user3['auth_user_id']})
    channel_details = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id_2}).json()
    assert response.status_code == 200
    assert response.json() == {}
    assert channel_details['owner_members'] == [
                                                    {
                                                        'u_id': create_user2['auth_user_id'],
                                                        'email': "z54626@unsw.edu.au",
                                                        'name_first': "Snickers",
                                                        'name_last': "Lickers",
                                                        'handle_str': "snickerslickers",
                                                    }  
                                                ]

# Test for when a member tries to remove an owner (no owner permissions) -> ACCESS ERROR
def test_member_removeowner(clear_store, create_user, create_user2, create_user3, create_user4):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    user_token_4 = create_user4['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(JOIN_URL, json = {'token': user_token_2, 'channel_id': channel_id_1})
    requests.post(JOIN_URL, json = {'token': user_token_3, 'channel_id': channel_id_1})
    requests.post(JOIN_URL, json = {'token': user_token_4, 'channel_id': channel_id_1})
    requests.post(ADDOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_1, 'u_id': create_user4['auth_user_id']})
    response_1 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_2, 'channel_id': channel_id_1, 'u_id': create_user4['auth_user_id']})
    response_2 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_3, 'channel_id': channel_id_1, 'u_id': create_user4['auth_user_id']})
    assert response_1.status_code == 403
    assert response_2.status_code == 403

# Test for when a user_token is invalid -> ACCESS ERROR
def test_invalid_user_token(clear_store, create_user, create_user2):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json = {'token': user_token})
    request_data = requests.post(REMOVEOWNER_URL, json = {'token': user_token, 'channel_id': channel_id, 'u_id': create_user2['auth_user_id']})
    assert request_data.status_code == 403

# Test for when a user_id is invalid -> INPUT ERROR
def test_invalid_u_id(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(REMOVEOWNER_URL, json = {'token': user_token, 'channel_id': channel_id, 'u_id': 24})
    assert response.status_code == 400

# Tests for when the user_id entered is not an owner of the channel -> INPUT ERROR
def test_u_id_not_owner(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    requests.post(JOIN_URL, json = {'token': user_token_2, 'channel_id': channel_id_1})
    requests.post(JOIN_URL, json = {'token': user_token_3, 'channel_id': channel_id_1})
    request_data_1 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_1, 'u_id': create_user3['auth_user_id']})
    request_data_2 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id_1, 'u_id': create_user2['auth_user_id']})

    assert request_data_1.status_code == 400
    assert request_data_2.status_code == 400

# Test for when the user_id is already a channel owner -> INPUT ERROR
def test_only_owner(clear_store, create_user):
    user_token = create_user['token']
    u_id = create_user['auth_user_id']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    request_data = requests.post(REMOVEOWNER_URL, json = {'token': user_token, 'channel_id': channel_id, 'u_id': u_id})
    assert request_data.status_code == 400

# Tests for when an invalid channel_id is entered -> INPUT ERROR
def test_invalid_channel_id(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    u_id_1 = create_user['auth_user_id']
    u_id_2 = create_user2['auth_user_id']
    channel_id = 15
    request_data_1 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_1, 'channel_id': channel_id, 'u_id': u_id_1})
    request_data_2 = requests.post(REMOVEOWNER_URL, json = {'token': user_token_2, 'channel_id': channel_id, 'u_id': u_id_2})
    assert request_data_1.status_code == 400
    assert request_data_2.status_code == 400
