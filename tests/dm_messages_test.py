from src.config import url
import pytest
import requests


CREATE_URL = f"{url}/channels/create/v2"
REGISTER_URL = f"{url}/auth/register/v2"
LOGOUT_URL = f"{url}/auth/logout/v1"
DM_CREATE_URL = f"{url}/dm/create/v1"
DM_SEND_URL = f"{url}/message/senddm/v1"
DM_MESSAGES_URL = f"{url}/dm/messages/v1"
DM_LIST_URL = f"{url}/dm/list/v1"


@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


@pytest.fixture
def register_user_1():
    response = requests.post(REGISTER_URL, json={"email": "z55555@unsw.edu.au", "password": "passwordlong", "name_first": "Jake", "name_last": "Renzella"}).json()
    return response


@pytest.fixture
def register_user_2():
    response = requests.post(REGISTER_URL, json={"email": "z12345@unsw.edu.au", "password": "epicpassword", "name_first": "FirstName", "name_last": "LastName"}).json()
    return response


def test_basic_success(clear_store, register_user_1):
    user_1 = register_user_1
    dm_id = requests.post(DM_CREATE_URL, json={'token': user_1['token'], 'u_ids':[]}).json()['dm_id']
    message_id = requests.post(DM_SEND_URL, json={'token': user_1['token'], 'dm_id': dm_id, 'message': "HEY ME"}).json()['message_id']
    response = requests.get(DM_MESSAGES_URL, params = {"token": user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert response.status_code == 200
    list_msg_ids = [message['message_id'] for message in response.json()['messages']]
    assert message_id in list_msg_ids
    msg_index = list_msg_ids.index(message_id)
    assert response.json()['messages'][msg_index]['message_id'] == message_id
    assert response.json()['messages'][msg_index]['u_id'] == user_1['auth_user_id']
    assert response.json()['messages'][msg_index]['message'] == "HEY ME"
    assert response.json()['start'] == 0
    assert response.json()['end'] == -1


def test_pagination_success(clear_store, register_user_1, register_user_2):
    user_1_token = register_user_1['token']
    user_2_id = register_user_2['auth_user_id']

    dm_id = requests.post(DM_CREATE_URL, json={"token": user_1_token, "u_ids": [user_2_id]}).json()['dm_id']

    for i in range(0, 124):
        requests.post(DM_SEND_URL, json={"token": user_1_token, "dm_id": dm_id, "message": str(i)})

    request_messages = requests.get(DM_MESSAGES_URL, params={"token": user_1_token, 'dm_id': dm_id, 'start': 0})
    counter = 123
    current_start = 0
    while request_messages.json()['end'] != -1:
        assert request_messages.json()['start'] == current_start
        assert request_messages.json()['end'] == current_start + 50
        assert len(request_messages.json()['messages']) == 50
        for message in request_messages.json()['messages']:
            assert message['message'] == str(counter)
            counter -= 1
        current_start += 50
        request_messages = requests.get(DM_MESSAGES_URL, params={"token": user_1_token, 'dm_id': dm_id, 'start': current_start})
    for message in request_messages.json()['messages']:
        assert message['message'] == str(counter)
        counter -= 1
    assert counter == -1



def test_invalid_dm_id(clear_store, register_user_1):
    user_1 = register_user_1
    dm_id = requests.post(DM_CREATE_URL, json={'token': user_1['token'], 'u_ids':[]}).json()['dm_id']
    response = requests.get(DM_MESSAGES_URL, params = {"token": user_1['token'], 'dm_id': dm_id + 1, 'start': 0})
    assert response.status_code == 400

def test_invalid_u_id(clear_store, register_user_1, register_user_2):
    user_1 = register_user_1
    user_2 = register_user_2
    dm_id = requests.post(DM_CREATE_URL, json={'token': user_1['token'], 'u_ids':[]}).json()['dm_id']
    response = requests.get(DM_MESSAGES_URL, params = {"token": user_2['token'], 'dm_id': dm_id, 'start': 0})
    assert response.status_code == 403


def test_invalid_start(clear_store, register_user_1):
    user_1 = register_user_1
    dm_id = requests.post(DM_CREATE_URL, json={'token': user_1['token'], 'u_ids':[]}).json()['dm_id']
    response = requests.get(DM_MESSAGES_URL, params = {"token": user_1['token'], 'dm_id': dm_id, 'start': 43})
    assert response.status_code == 400
