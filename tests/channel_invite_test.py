from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.auth import auth_register_v1 
from src.error import InputError, AccessError
from src.other import clear_v1

import pytest

@pytest.fixture
def clear_store():
    clear_v1()

@pytest.fixture
def create_user():
    user_id = auth_register_v1("z4323234@unsw.edu.au", "password", "Name1", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_user2():
    user_id = auth_register_v1("z546326@unsw.edu.au", "password", "Name2", "Lastname")['auth_user_id']
    return user_id

@pytest.fixture
def create_user3():
    user_id = auth_register_v1("z5362601@unsw.edu.au", "password", "Name3", "Lastname")['auth_user_id']
    return user_id


def check_user(auth_user_id, u_id, channel_id):
    details = channel_details_v1(auth_user_id, channel_id)

    user_was_added = False
    members = details['all_members']
    for member in members:
        if member['u_id'] == u_id:
            user_was_added = True

    return user_was_added


def test_invite_public(clear_store, create_user, create_user2):
    auth_user_id = create_user
    channel_id = channels_create_v1(auth_user_id, 'Channel1', True)['channel_id']
    u_id = create_user2
    channel_invite_v1(auth_user_id, channel_id, u_id)
    
    # Check if u_id is now in channel
    assert check_user(auth_user_id, u_id, channel_id)

def test_invite_private(clear_store, create_user, create_user2):
    auth_user_id = create_user
    channel_id = channels_create_v1(auth_user_id, 'Channel1', False)['channel_id']
    u_id = create_user2
    channel_invite_v1(auth_user_id, channel_id, u_id)
    
    # Check if u_id is now in channel
    assert check_user(auth_user_id, u_id, channel_id)

# Inviting multiple users to multiple channels & invited users inviting users
def test_invite_multiple(clear_store, create_user, create_user2, create_user3):
    auth_user_id = create_user
    channel_id_1 = channels_create_v1(auth_user_id, 'Channel1', False)['channel_id']
    channel_id_2 = channels_create_v1(auth_user_id, 'Channel2', True)['channel_id']
    u_id_1 = create_user2
    u_id_2 = create_user3
    channel_invite_v1(auth_user_id, channel_id_1, u_id_1)

    assert check_user(auth_user_id, u_id_1, channel_id_1)

    channel_invite_v1(u_id_1, channel_id_1, u_id_2)
    channel_invite_v1(auth_user_id, channel_id_2, u_id_2)
    
    # Check if u_id is now in channel
    assert check_user(auth_user_id, u_id_2, channel_id_2)
    assert check_user(auth_user_id, u_id_2, channel_id_2)

#-------------------------Error Testing------------------------------#

# Access error when auth_user_id is invalid
def test_invite_auth_user_id_invalid(clear_store, create_user, create_user2):
    auth_user_id = create_user
    u_id = create_user2
    channel_id = channels_create_v1(auth_user_id, 'Channel1', True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(None, channel_id, u_id)

# channel_id is not a valid channel
def test_invite_error_invalid_channel(clear_store, create_user, create_user2):
    auth_user_id = create_user
    u_id = create_user2
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, None, u_id)

# u_id is not a valid user
def test_invite_error_invalid_user(clear_store, create_user):
    auth_user_id = create_user
    channel_id = channels_create_v1(auth_user_id, 'Channel1', True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, None)

# u_id refers to a member who is already in channel
def test_invite_error_already_joined(clear_store, create_user, create_user2):
    auth_user_id = create_user
    u_id = create_user2
    channel_id = channels_create_v1(auth_user_id, 'Channel1', True)['channel_id']
   
    channel_join_v1(u_id, channel_id)
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, u_id)

# channel_id is valid but authorised user is not member of channel
def test_invite_error_not_member(clear_store, create_user, create_user2, create_user3):
    auth_user_id_1 = create_user
    auth_user_id_2 = create_user2
    u_id = create_user3
    channel_id = channels_create_v1(auth_user_id_1, 'Channel1', True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user_id_2, channel_id, u_id)