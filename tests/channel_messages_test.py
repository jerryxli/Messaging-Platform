import pytest

from src.auth import auth_register_v1
from src.channel import channel_messages_v1
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

def test_invalid_channel_id(clear_store, create_user):
    user_id = create_user
    with pytest.raises(InputError):
        channel_messages_v1(user_id, 1, 0)

def test_user_not_in_channel(clear_store, create_user, create_user2):
    user_id = create_user
    user_id2 = create_user2
    channel_id = channels_create_v1(user_id, 'test', True)
    with pytest.raises(AccessError):
        channel_messages_v1(user_id2, channel_id['channel_id'], 0)

def test_channel_messages_with_no_messages(clear_store, create_user):
    user_id = create_user
    channel_id = channels_create_v1(user_id, 'test', True)
    expected_output = { 'messages': [], 'start': 0, 'end': -1 }
    assert channel_messages_v1(user_id, channel_id['channel_id'], 0) == expected_output
