from src.channels import channels_list_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1

import pytest

@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_id = auth_register_v1("z432324@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_user2():
    user_id = auth_register_v1("z54626@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_user3():
    user_id = auth_register_v1("z536601@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_id

# When channels_list_v1 is called, it should return the channel name and channel id.
# In the format: {'channel_id': ' ', 'name': ' '}

# Test for when the user has no channels
def test_no_channels(clear_store, create_user):
    user_id = create_user
    expected_outcome = { 'channels': [] }
    assert channels_list_v1(user_id) == expected_outcome

# Test for when the user has created one channel
def test_one_channel(clear_store, create_user):
    user_id = create_user
    channel_id = channels_create_v1(user_id, 'Name', True)['channel_id']
    expected_outcome = { 'channels': [{'channel_id': channel_id, 'name': 'Name'}] }
    assert channels_list_v1(user_id) == expected_outcome

# Test for when the user has multiple channels
def test_multiple_channels(clear_store, create_user):
    user_id = create_user
    channel_id_1 = channels_create_v1(user_id, 'Name 1', True)['channel_id']
    channel_id_2 = channels_create_v1(user_id, 'Name 2', False)['channel_id']
    channel_id_3 = channels_create_v1(user_id, 'Name 3', True)['channel_id']
    expected_outcome = { 'channels': [{'channel_id': channel_id_1, 'name': 'Name 1'}, {'channel_id': channel_id_2, 'name': 'Name 2'}, {'channel_id': channel_id_3, 'name': 'Name 3'}] }
    assert channels_list_v1(user_id) == expected_outcome

# Test for when multiple users have created channels
def test_multiple_users(clear_store, create_user, create_user2, create_user3):
    user_id_1 = create_user
    user_id_2 = create_user2
    user_id_3 = create_user3

    channel_id_1 = channels_create_v1(user_id_1, 'Name 1', True)['channel_id']
    channel_id_2 = channels_create_v1(user_id_2, 'Name 2', False)['channel_id']
    channel_id_3 = channels_create_v1(user_id_3, 'Name 3', True)['channel_id']
    assert channels_list_v1(user_id_1) == { 'channels': [{'channel_id': channel_id_1, 'name': 'Name 1'}] }
    assert channels_list_v1(user_id_2) == { 'channels': [{'channel_id': channel_id_2, 'name': 'Name 2'}] }
    assert channels_list_v1(user_id_3) == { 'channels': [{'channel_id': channel_id_3, 'name': 'Name 3'}] }

