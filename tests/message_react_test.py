from src.config import url
import pytest
import requests
import src.other as other


@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})


@pytest.fixture
def create_user():
    user_input = {'email': "z432324@unsw.edu.au",
                  'password': "badpassword123", 'name_first': "Ji", 'name_last': "Sun"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info


def test_basic_message_react(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(other.MESSAGE_SEND_URL, json={
                               'token': user_token_1, 'channel_id': channel_id, 'message': "yay react works"}).json()['message_id']
    response = requests.post(other.MESSAGE_REACT_URL, json={
                             'token': user_token_1, 'message_id': message_id, 'react_id': 1})
    assert response.status_code == 200


def test_message_id_invalid(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(other.MESSAGE_SEND_URL, json={
                               'token': user_token_1, 'channel_id': channel_id, 'message': "message id invalid"}).json()['message_id']
    response = requests.post(other.MESSAGE_REACT_URL, json={
                             'token': user_token_1, 'message_id': int(message_id) + 1, 'react_id': 1})
    assert response.status_code == 400


def test_react_id_invalid(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(other.MESSAGE_SEND_URL, json={
                               'token': user_token_1, 'channel_id': channel_id, 'message': "react id invalid"}).json()['message_id']
    response = requests.post(other.MESSAGE_REACT_URL, json={
                             'token': user_token_1, 'message_id': message_id, 'react_id': 0})
    assert response.status_code == 400


def test_message_contains_react_already(clear_store, create_user):
    user_token_1 = create_user['token']
    channel_id = requests.post(other.CHANNELS_CREATE_URL, json={
                               'token': user_token_1, 'name': 'My Channel!', 'is_public': True}).json()['channel_id']

    message_id = requests.post(other.MESSAGE_SEND_URL, json={
                               'token': user_token_1, 'channel_id': channel_id, 'message': "already reacted to"}).json()['message_id']
    response = requests.post(other.MESSAGE_REACT_URL, json={
                             'token': user_token_1, 'message_id': message_id, 'react_id': 1})
    assert response.status_code == 200
    response = requests.post(other.MESSAGE_REACT_URL, json={
                             'token': user_token_1, 'message_id': message_id, 'react_id': 1})
    assert response.status_code == 400
