from src.config import url
import pytest
import requests

CHANNEL_JOIN_URL = f"{url}/channel/join/v2"
CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
CHANNEL_MESSAGES_URL = f"{url}/channel/messages/v2"


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


# def test_invalid_channel_id(clear_store, create_user):
#     user_token_1 = create_user
#     with pytest.raises(InputError):
#         channel_messages_v1(user_token_1, 1, 0)

# def test_user_not_in_channel(clear_store, create_user, create_user2):
#     user_token_1 = create_user
#       user_token_2 = create_user2
#     channel_id = channels_create_v1(user_token_1, 'test', True)
#     with pytest.raises(AccessError):
#         channel_messages_v1   user_token_2, channel_id['channel_id'], 0)

# def test_channel_messages_with_no_messages(clear_store, create_user):
#     user_token_1 = create_user
#     channel_id = channels_create_v1(user_token_1, 'test', True)
#     expected_output = { 'messages': [], 'start': 0, 'end': -1 }
#     assert channel_messages_v1(user_token_1, channel_id['channel_id'], 0) == expected_output

# def test_channel_messages_start_exceeds(clear_store, create_user):
#      user_token_1 = create_user
#      channel_id = channels_create_v1(user_token_1, 'test', True)['channel_id']

#      current = 0
#      messages = channel_messages_v1(user_token_1, channel_id, current)
#      # Spew through the messages until we reach the end
#      while messages['end'] != -1:
#          current += 50
#          messages = channel_messages_v1(user_token_1, channel_id, current)

#      with pytest.raises(InputError):
#         channel_messages_v1(user_token_1, channel_id, current+100)


# def test_invalid_auth_id(clear_store, create_user):
#     user_token_1 = create_user
#     fake_id = user_token_1 + 1
#     channel_id = channels_create_v1(user_token_1, "Cool", True)['channel_id']
#     with pytest.raises(AccessError):
#         channel_messages_v1(fake_id, channel_id, 0)


def test_invalid_channel_id(clear_store, create_user):
    user_token_1 = create_user
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'user_token': user_token_1, 'channel_id': 1, 'start': 0})
    assert response.status_code != 200


def test_user_not_in_channel(clear_store, create_user, create_user2):
    user_token_1 = create_user
    user_token_2 = create_user2
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'user_token': user_token_2, 'channel_id': channel_id, 'start': 0})
    assert response.status_code != 200


def test_channel_messages_with_no_messages(clear_store, create_user):
    user_token_1 = create_user
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'user_token': user_token_1, 'channel_id': channel_id, 'start': 0})
    expected_output = {'messages': [], 'start': 0, 'end': -1}
    assert response.json() == expected_output
    assert response.status_code == 200


def test_channel_messages_start_exceeds(clear_store, create_user):
    user_token_1 = create_user
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']
    current = 0
    response = requests.get(CHANNEL_MESSAGES_URL, params={'user_token': user_token_1,
                                                          'channel_id': channel_id, 'start': current})
    # Spew through the messages until we reach the end
    while response.json(['end']) != -1:
        current += 50
        response = requests.get(CHANNEL_MESSAGES_URL, params={'user_token': user_token_1,
                                                              'channel_id': channel_id, 'start': current})
    response = requests.get(CHANNEL_MESSAGES_URL, params={'user_token': user_token_1,
                                                          'channel_id': channel_id, 'start': current + 100})
    assert response.status_code != 200


def test_invalid_auth_id(clear_store, create_user):
    user_token_1 = create_user
    fake_id = user_token_1 + 1
    channel_id = requests.post(CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    response = requests.get(CHANNEL_MESSAGES_URL, params={
                            'user_token': fake_id, 'channel_id': channel_id, 'start': 0})
    assert response.status_code != 200
