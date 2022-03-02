import pytest
import datetime

from src.channel import channel_messages_v1, check_user_in_channel, get_channel
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def register_owner():
    user_id = auth_register_v1("z432324@unsw.edu.au", "password", "Name", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_channel(user_id):
    channel_id = channels_create_v1(user_id, 'test', True)
    return channel_id

@pytest.fixture
def create_user2():
    user_id2 = auth_register_v1("z432325@unsw.edu.au", "password1", "Name1", "Lastname1")['auth_user_id']
    return user_id2 


def invalid_channel_id(clear_v1, register_owner):
    user_id = register_owner()
    with pytest.raises(InputError):
        channel_messages_v1(user_id, 1, "1")

def start_greater_than_messages(clear_v1, register_owner, create_channel):
    user_id = register_owner()
    channel_id = create_channel(user_id)

def user_not_in_channel(clear_v1, register_owner, create_user2, create_channel):
    user_id = register_owner()
    user_id2 = create_user2()
    channel_id = create_channel(user_id)
    with pytest.raises(AccessError):
        channel_messages_v1(user_id2, channel_id, "1")



