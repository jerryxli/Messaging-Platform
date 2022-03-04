from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1, is_valid_dictionary_output
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
    user_id = auth_register_v1("z536362@unsw.edu.au", "password", "Eman", "Emantsal")['auth_user_id']
    return user_id

@pytest.fixture
def create_user3():
    user_id = auth_register_v1("z535436@unsw.edu.au", "password", "Name3", "Lastname3")['auth_user_id']
    return user_id

# The channels_details_v1 function takes in user_id and channel_id as input.
# The function then outputs { name: , is_public: , owner_members: , all_members: } for the channel.

# Tests for the creator trying to access the details of a channel with only one member (themselves).
def test_creator_of_channel(clear_store, create_user, create_user2):
    user_id_1 = create_user
    user_id_2 = create_user2
    channel_id_1 = channels_create_v1(user_id_1, 'Channel_Name', True)['channel_id']
    channel_id_2 = channels_create_v1(user_id_2, 'Channel_Name2', False)['channel_id']
    assert is_valid_dictionary_output(channel_details_v1(user_id_1, channel_id_1), {'name': str, 'owner_members': list, 'all_members': list})
    for user in channel_details_v1(user_id_1, channel_id_1)['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_v1(user_id_1, channel_id_1)['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})
    
    assert is_valid_dictionary_output(channel_details_v1(user_id_2, channel_id_2), {'name': str, 'owner_members': list, 'all_members': list})
    for user in channel_details_v1(user_id_2, channel_id_2)['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_v1(user_id_2, channel_id_2)['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})


    
# Tests for a member and creator getting details of a private channel
def test_member_of_public_channel(clear_store, create_user, create_user2):
    user_id_1 = create_user
    user_id_2 = create_user2
    channel_id = channels_create_v1(user_id_1, 'Channel_Name', True)['channel_id']
    channel_join_v1(user_id_2, channel_id)
    assert is_valid_dictionary_output(channel_details_v1(user_id_1, channel_id), {'name': str, 'owner_members': list, 'all_members': list})
    for user in channel_details_v1(user_id_1, channel_id)['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_v1(user_id_1, channel_id)['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    assert is_valid_dictionary_output(channel_details_v1(user_id_2, channel_id), {'name': str,'owner_members': list, 'all_members': list})
    for user in channel_details_v1(user_id_2, channel_id)['owner_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    for user in channel_details_v1(user_id_2, channel_id)['all_members']:
        assert is_valid_dictionary_output(user, {'name_first': str, 'name_last': str, 'email': str, 'handle_str': str, 'u_id': int})

    assert channel_details_v1(user_id_2, channel_id) == channel_details_v1(user_id_1, channel_id)


def test_invalid_member(clear_store, create_user):
    user_id = create_user
    channel_id = channels_create_v1(user_id, 'Channel_Name', True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(user_id + 40, channel_id)

# Tests for when the user_id entered is not a member of the channel_id.
def test_unauthorised_user_id(clear_store, create_user, create_user2, create_user3):
    user_id_1 = create_user
    user_id_2 = create_user2
    user_id_3 = create_user3
    channel_id_1 = channels_create_v1(user_id_1, 'Channel_Name', False)['channel_id']
    channel_id_2 = channels_create_v1(user_id_1, 'Channel_Name1', True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(user_id_2, channel_id_1)
    with pytest.raises(AccessError):
        channel_details_v1(user_id_3, channel_id_2)

def test_double_channel_name(clear_store, create_user):
    user_id_1 = create_user
    channel_id_1 = channels_create_v1(user_id_1, 'Channel_Name', False)['channel_id']
    with pytest.raises(InputError):
        channels_create_v1(user_id_1, 'Channel_Name', True)['channel_id']

# Tests for when an invalid channel_id is entered.
def test_invalid_channel_id(clear_store, create_user, create_user2):
    user_id_1 = create_user
    user_id_2 = create_user2
    channel_id = 0
    with pytest.raises(InputError):
        channel_details_v1(user_id_1, channel_id)
    with pytest.raises(InputError):
        channel_details_v1(user_id_2, channel_id)
