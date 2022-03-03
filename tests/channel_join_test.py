import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_id = auth_register_v1("z432324@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_id  

@pytest.fixture
def create_user2():
    user_id2 = auth_register_v1("z432325@unsw.edu.au", "password1", "Name1", "Lastname1")['auth_user_id']
    return user_id2 

@pytest.fixture
def create_user3():
    user_id3 = auth_register_v1("z432326@unsw.edu.au", "password2", "Name2", "Lastname2")['auth_user_id']
    return user_id3 

def test_private_channel(clear_store, create_user, create_user2):
    user_id = create_user
    user_id2 = create_user2
    channels = channels_create_v1(user_id, 'test2', False)
    with pytest.raises(AccessError):
        channel_join_v1(user_id2, channels['channel_id']) 

def test_successfully_joined_channel(clear_store, create_user, create_user2):
    user_id = create_user
    user_id2 = create_user2
    channel_id = channels_create_v1(user_id, 'test2', True)
    expected_outcome = None
    channel_join_v1(user_id2, channel_id['channel_id'])
    assert channel_details_v1(user_id2, channel_id['channel_id'])

def test_successfully_joined_channel2(clear_store, create_user, create_user2, create_user3):
    user_id = create_user
    user_id2 = create_user2
    user_id3 = create_user3
    channel_id = channels_create_v1(user_id, 'test2', True)
    channel_join_v1(user_id2, channel_id['channel_id']) 
    channel_join_v1(user_id3, channel_id['channel_id']) 
    assert channel_details_v1(user_id2, channel_id['channel_id'])
    assert channel_details_v1(user_id3, channel_id['channel_id'])

def test_channel_doesnt_exist(clear_store, create_user, create_user2):
    user_id = create_user
    with pytest.raises(InputError):
        channel_join_v1(user_id, 0)    

def test_user_already_in_channel(clear_store, create_user, create_user2):
    user_id = create_user
    channels = channels_create_v1(user_id, 'test2', True)
    with pytest.raises(InputError):
        channel_join_v1(user_id, channels['channel_id'])
