from src.error import AccessError
from src.config import port, url
from .helper_functions import is_valid_dictionary_output
import requests
import pytest

DETAILS_URL = f"{url}/channel/details/v2"
JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})

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
def create_user3():
    user_input = {'email': "z536601@unsw.edu.au", 'password': "1243Bops", 'name_first': "Mars", 'name_last': "Bars"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

@pytest.fixture
def create_stub_user():
    user_input = {'email': "example@gmail.com", 'password': "hello123", 'name_first': "Hayden",'name_last': "Jacobs"}
    user_info = requests.post(REGISTER_URL, json = user_input).json()
    return user_info

# The channels_details_v1 function takes in user_id and channel_id as input.
# The function then outputs { name: , is_public: , owner_members: , all_members: } for the channel.
# Tests for the creator trying to access the details of a channel with only one member (themselves).
def test_creator_of_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'kitchen', 'is_public': False}).json()['channel_id']
    channel_details_1 = requests.get(DETAILS_URL, params = {'token': user_token_1, 'channel_id': channel_id_1}).json()
    channel_details_2 = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id_2}).json()

    assert is_valid_dictionary_output(channel_details_1, {'name': str, 'is_public': bool, 'owner_members': list, 'all_members': list})
    for user in channel_details_1['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_1['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})
    
    assert is_valid_dictionary_output(channel_details_2, {'name': str, 'is_public': bool, 'owner_members': list, 'all_members': list})
    for user in channel_details_2['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_2['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})


# Tests for a member and creator getting details of a private channel
def test_member_of_public_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_join = requests.post(JOIN_URL, json = {'token': user_token_2, 'channel_id': channel_id}).json()
    channel_details_1 = requests.get(DETAILS_URL, params = {'token': user_token_1, 'channel_id': channel_id}).json()
    channel_details_2 = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id}).json()
    expected_output =  {   'name': 'My Channel!', 
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
                                },
                                {
                                    'u_id': create_user2['auth_user_id'],
                                    'email': "z54626@unsw.edu.au",
                                    'name_first': "Snickers",
                                    'name_last': "Lickers",
                                    'handle_str': "snickerslickers",
                                },
                            ],
                        }
    
    assert channel_join == {}
    

    assert channel_details_1 == expected_output
    assert channel_details_2 == expected_output
    

# Test for when a user_token is invalid
def test_invalid_user(clear_store, create_user):
    user_token = create_user['token']
    channel_id = requests.post(CREATE_URL, json = {'token': user_token, 'name': 'Channel!', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json = {'token': user_token})
    request_data = requests.get(DETAILS_URL, params = {'token': user_token, 'channel_id': channel_id})
    assert request_data.status_code == 403


# Tests for when the user_id entered is not a member of the channel_id.
def test_unauthorised_user_id(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id_1 = requests.post(CREATE_URL, json = {'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    channel_id_2 = requests.post(CREATE_URL, json = {'token': user_token_2, 'name': 'kitchen', 'is_public': False}).json()['channel_id']
    request_data_1 = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id_1})
    request_data_2 = requests.get(DETAILS_URL, params = {'token': user_token_3, 'channel_id': channel_id_2})
    # Access Error
    assert request_data_1.status_code == 403
    assert request_data_2.status_code == 403


# Tests for when an invalid channel_id is entered.
def test_invalid_channel_id(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = 0
    request_data_1 = requests.get(DETAILS_URL, params = {'token': user_token_1, 'channel_id': channel_id})
    request_data_2 = requests.get(DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id})
    # Input Error
    assert request_data_1.status_code == 400
    assert request_data_2.status_code == 400


# Test against the stub code output
def test_from_stub_code(clear_store, create_stub_user):
    stub_token = create_stub_user['token']
    stub_uid = create_stub_user['auth_user_id']
    channel_id = requests.post(CREATE_URL, json = {'token': stub_token, 'name': "Hayden", 'is_public': False}).json()['channel_id']
    channel_details = requests.get(DETAILS_URL, params = {'token': stub_token, 'channel_id': channel_id})
    assert channel_details.json() ==  {
        'name': 'Hayden',
        'is_public': False,
        'owner_members': [
            {
                'u_id': stub_uid,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': stub_uid,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }