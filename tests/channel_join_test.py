from src.config import url
import pytest
import requests

CHANNEL_JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
CHANNEL_DETAILS_URL = f"{url}/channel/details/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
LISTALL_URL = f"{url}/channels/listall/v2"
LIST_URL = f"{url}/channels/list/v2"


@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au",
                  'password': "password", 'name_first': "Name", 'name_last': "Lastname"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


@pytest.fixture
def create_user2():
    user_input = {'email': "z432325@unsw.edu.au", 'password': "password1",
                  'name_first': "Name1", 'name_last': "Lastname1"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


@pytest.fixture
def create_user3():
    user_input = {'email': "z432326@unsw.edu.au",
                  'password': "password2", 'name_first': "Name2", 'name_last': "Lastname2"}
    request_data = requests.post(REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


def test_private_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': False}).json()['channel_id']
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})
    assert response.status_code == 403


def test_successfully_joined_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'test', 'is_public': True}).json()['channel_id']
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})
    assert response.status_code == 200
    channel_details = requests.get(CHANNEL_DETAILS_URL, params = {'token': user_token_2, 'channel_id': channel_id}).json()
    expected_outcome = {
        'name': 'test',
        'is_public': True,
        'owner_members': [
            {
                'u_id': create_user['auth_user_id'],
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            }
        ],
        'all_members': [
            {
                'u_id': create_user['auth_user_id'],
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            },
            {
                'u_id': create_user2['auth_user_id'],
                'email': 'z432325@unsw.edu.au',
                'name_first': 'Name1',
                'name_last': 'Lastname1',
                'handle_str': 'name1lastname1',
            },
        ]
    }
    assert channel_details == expected_outcome


def test_successfully_joined_channel2(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'test2', 'is_public': True}).json()['channel_id']
    response_1 = requests.post(CHANNEL_JOIN_URL, json={
                               'token': user_token_2, 'channel_id': channel_id})
    assert response_1.status_code == 200
    response_2 = requests.post(CHANNEL_JOIN_URL, json={
                               'token': user_token_3, 'channel_id': channel_id})
    assert response_2.status_code == 200
    channel_details = requests.get(CHANNEL_DETAILS_URL, params = {'token': user_token_3, 'channel_id': channel_id}).json()
    expected_outcome = {
        'name': 'test2',
        'is_public': True,
        'owner_members': [
            {
                'u_id': create_user['auth_user_id'],
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            }
        ],
        'all_members': [
            {
                'u_id': create_user['auth_user_id'],
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            },
            {
                'u_id': create_user2['auth_user_id'],
                'email': 'z432325@unsw.edu.au',
                'name_first': 'Name1',
                'name_last': 'Lastname1',
                'handle_str': 'name1lastname1',
            },
            {
                'u_id': create_user3['auth_user_id'],
                'email': 'z432326@unsw.edu.au',
                'name_first': 'Name2',
                'name_last': 'Lastname2',
                'handle_str': 'name2lastname2',
            },
        ],
    }
    assert channel_details == expected_outcome


def test_channel_doesnt_exist(clear_store, create_user):
    user_token_1 = create_user['token']
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_1, 'channel_id': 0})
    assert response.status_code == 400


def test_user_already_in_channel(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_1, 'channel_id': channel_id})
    assert response.status_code == 400


def test_list_and_join(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'test2', 'is_public': True}).json()['channel_id']

    assert requests.get(LIST_URL, params = {'token': user_token_1}).json() == {'channels': [{'channel_id': channel_id,'name': 'test2'}]}
    assert requests.get(LISTALL_URL, params = {'token': user_token_2}).json() == requests.get(LIST_URL, params = {'token': user_token_1}).json()
    assert requests.get(LIST_URL, params = {'token': user_token_2}).json() == {'channels': []}
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})
    assert response.status_code == 200
    assert requests.get(LIST_URL, params = {'token': user_token_2}).json() == {'channels': [{'channel_id': channel_id,'name': 'test2'}]}

def test_global_owner_join_private(clear_store, create_user, create_user2, create_user3):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    user_token_3 = create_user3['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_2, 'name': 'secret', 'is_public': False}).json()['channel_id']
    #  Test normal member cant get in
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_3, 'channel_id': channel_id})
    assert response.status_code == 403
    # Verify owner is not in the channel
    assert requests.get(LIST_URL, params = {'token': user_token_1}).json() == {'channels': []}
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_1, 'channel_id': channel_id})
    assert response.status_code == 200
    assert requests.get(LIST_URL, params = {'token': user_token_1}).json() == {'channels': [{'channel_id': channel_id,'name': 'secret'}]}


def test_fake_id(clear_store, create_user, create_user2):
    user_token_1 = create_user['token']
    user_token_2 = create_user2['token']
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'test2', 'is_public': True}).json()['channel_id']
    requests.post(LOGOUT_URL, json={'token': user_token_2})
    response = requests.post(CHANNEL_JOIN_URL, json={
                             'token': user_token_2, 'channel_id': channel_id})
    assert response.status_code == 403
