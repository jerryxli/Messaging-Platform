from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.other import clear_v1

import pytest

@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_id = auth_register_v1("z2537530@unsw.edu.au", "password", "Firstname", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_user2():
    user_id = auth_register_v1("z934183@unsw.edu.au", "password", "Firstname", "Lastname")['auth_user_id']
    return user_id

# Access error when auth_user_id is invalid
def test_listall_auth_user_id_invalid(clear_store):
    with pytest.raises(AccessError):
        channels_listall_v1(None)

# Test for when there are no channels
def test_listall_no_channels(clear_store, create_user):
    user_id = create_user
    assert channels_listall_v1(user_id) == {'channels': []} 

# Test for when there is only one public channel
def test_listall_one_public(clear_store, create_user):
    user_id = create_user
    channels_create_v1(user_id, 'Channel1', True)
    assert channels_listall_v1(user_id) == {'channels': [{'channel_id': 0, 'name': 'Channel1'}]}
    
# Test for when there is only one private channel
def test_listall_one_private(clear_store, create_user):
    user_id = create_user
    channels_create_v1(user_id, 'Channel1', False)
    assert channels_listall_v1(user_id) == {'channels': [{'channel_id': 0, 'name': 'Channel1'}]}

# Test for when there are multiple private channel
def test_listall_mul_private(clear_store, create_user):
    user_id = create_user
    channels_create_v1(user_id, 'Channel1', False)
    channels_create_v1(user_id, 'Channel2', False)
    assert channels_listall_v1(user_id) == {'channels': [{'channel_id': 0, 'name': 'Channel1'}, {'channel_id': 1, 'name': 'Channel2'}]}
    
# Test for when there are multiple public and private channel
def test_listall_both_privacy(clear_store, create_user):
    user_id = create_user
    channels_create_v1(user_id, 'Channel1', True)
    channels_create_v1(user_id, 'Channel2', False)
    channels_create_v1(user_id, 'Channel3', False)
    channels_create_v1(user_id, 'Channel4', True)
    
    assert channels_listall_v1(user_id) == {'channels': [{'channel_id': 0, 'name': 'Channel1'}, {'channel_id': 1, 'name': 'Channel2'}, {'channel_id': 2, 'name': 'Channel3'}, {'channel_id': 3, 'name': 'Channel4'}]}

#--------- Test for channels user isin't part of -----------#

# Test for public and private channels user isin't part of
def test_listall_notin_bothprivacy(clear_store, create_user, create_user2):
    user_id_1 = create_user
    user_id_2 = create_user2
    channels_create_v1(user_id_1, 'Channel1', True)
    channels_create_v1(user_id_1, 'Channel2', False)
    channels_create_v1(user_id_2, 'Channel3', False)
    channels_create_v1(user_id_2, 'Channel4', True)
    expected = {'channels': [{'channel_id': 0, 'name': 'Channel1'}, {'channel_id': 1, 'name': 'Channel2'}, {'channel_id': 2, 'name': 'Channel3'}, {'channel_id': 3, 'name': 'Channel4'}]}
    assert channels_listall_v1(user_id_1) == expected
    assert channels_listall_v1(user_id_2) == expected
    

