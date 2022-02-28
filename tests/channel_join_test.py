import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1, is_public_channel
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1, verify_user

@pytest.fixture
def clear_store():
    clear_v1()

def test_public_channel_true(clear_store):
    auth_register_v1("hello@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    channel_id_public = channels_create_v1(0, 'test1', False)
    assert is_public_channel(channel_id_public) == True    

def test_public_channel_false(clear_store):
    auth_register_v1("hello@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    channel_id_private = channels_create_v1(0, 'test2', True)
    with pytest.raises(AccessError):
        is_public_channel(channel_id_private)

def test_successfully_joined_channel():
    auth_register_v1("hello@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    channels = channels_create_v1(0, 'test2', False)
    channel_join_v1(0, channels['channel_id']) 
    assert len(channels['users']) == 1

def test_channel_doesnt_exist():
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs")
    with pytest.raises(InputError):
        channel_join_v1(0, 0)    

def test_user_already_in_channel():
    auth_register_v1("hello@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    channels = channels_create_v1(0, 'test2', False)
    channel_join_v1(0, channels['channel_id']) 
    with pytest.raises(InputError):
        channel_join_v1(0, channels['channel_id'])

