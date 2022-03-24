from src.channels import channels_create_v1 
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from .helper_functions import is_valid_dictionary_output
import pytest

@pytest.fixture
def clear_store():
    clear_v1()


def test_add_public_channel(clear_store):
    user_id = auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")['auth_user_id']
    print(user_id)
    assert is_valid_dictionary_output(channels_create_v1(user_id, 'Jake\'s Room', True), {'channel_id': int})

def test_add_private_channel(clear_store):
    user_id = auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")['auth_user_id']
    assert is_valid_dictionary_output(channels_create_v1(user_id, 'My Happy place', True), {'channel_id': int})
    assert is_valid_dictionary_output(channels_create_v1(user_id, 'Woweeee', False), {'channel_id': int})

def test_null_name(clear_store):
    user_id = auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")['auth_user_id']
    with pytest.raises(InputError):
        channels_create_v1(user_id, '', False)

def test_long_name(clear_store):
    user_id = auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")['auth_user_id']
    with pytest.raises(InputError):
        channels_create_v1(user_id, 'abcdefghijklmnopqrstuvwxyzabcdef', False)

def test_invalid_user(clear_store):
    with pytest.raises(AccessError):
        channels_create_v1(1, 'apple', True)


