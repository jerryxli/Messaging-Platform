from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channels import channels_list_all_v1
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
def test_list_all_auth_user_id_invalid(clear_store):
    with pytest.raises(AccessError):
        channels_list_all_v1(None)

# Test for when there are no channels
def test_list_all_no_channels(clear_store, create_user):
    user_id = create_user
    assert channels_list_all_v1(user_id) == {'channels': []} 

# Test for when there is only one public channel
def test_list_all_one_public(clear_store, create_user):
    user_id = create_user
    channel_id = channels_create_v1(user_id, 'Channel1', True)['channel_id']
    assert channels_list_all_v1(user_id) == {'channels': [{'channel_id': channel_id, 'name': 'Channel1'}]}
    
# Test for when there is only one private channel
def test_list_all_one_private(clear_store, create_user):
    user_id = create_user
    channel_id = channels_create_v1(user_id, 'Channel1', False)['channel_id']
    assert channels_list_all_v1(user_id) == {'channels': [{'channel_id': channel_id, 'name': 'Channel1'}]}

# Test for when there are multiple private channel
def test_list_all_mul_private(clear_store, create_user):
    user_id = create_user
    channel_id1 = channels_create_v1(user_id, 'Channel1', False)['channel_id']
    channel_id2 = channels_create_v1(user_id, 'Channel2', False)['channel_id']
    assert channels_list_all_v1(user_id) == {'channels': [{'channel_id': channel_id1, 'name': 'Channel1'}, {'channel_id': channel_id2, 'name': 'Channel2'}]}
    
# Test for when there are multiple public and private channel
def test_list_all_both_privacy(clear_store, create_user):
    user_id = create_user
    channel_id1 = channels_create_v1(user_id, 'Channel1', True)['channel_id']
    channel_id2 = channels_create_v1(user_id, 'Channel2', False)['channel_id']
    channel_id3 = channels_create_v1(user_id, 'Channel3', False)['channel_id']
    channel_id4 = channels_create_v1(user_id, 'Channel4', True)['channel_id']
    
    assert channels_list_all_v1(user_id) == {'channels': [{'channel_id': channel_id1, 'name': 'Channel1'}, {'channel_id': channel_id2, 'name': 'Channel2'}, {'channel_id': channel_id3, 'name': 'Channel3'}, {'channel_id': channel_id4, 'name': 'Channel4'}]}

#--------- Test for channels user isin't part of -----------#

# Test for public and private channels user isin't part of
def test_list_all_notin_bothprivacy(clear_store, create_user, create_user2):
    user_id_1 = create_user
    user_id_2 = create_user2
    channel_id1 = channels_create_v1(user_id_1, 'Channel1', True)['channel_id']
    channel_id2 = channels_create_v1(user_id_1, 'Channel2', False)['channel_id']
    channel_id3 = channels_create_v1(user_id_2, 'Channel3', False)['channel_id']
    channel_id4 = channels_create_v1(user_id_2, 'Channel4', True)['channel_id']
    expected = {'channels': [{'channel_id': channel_id1, 'name': 'Channel1'}, {'channel_id': channel_id2, 'name': 'Channel2'}, {'channel_id':  channel_id3, 'name': 'Channel3'}, {'channel_id': channel_id4, 'name': 'Channel4'}]}
    assert channels_list_all_v1(user_id_1) == expected
    assert channels_list_all_v1(user_id_2) == expected
    

