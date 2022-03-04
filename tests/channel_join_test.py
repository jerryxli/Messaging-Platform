import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
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
    expected_outcome = {
        'name': 'test2',
        'owner_members': [
            {
                'u_id': user_id,
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            }
        ],
        'all_members': [
            {
                'u_id': user_id,
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            },
            {
                'u_id': user_id2,
                'email': 'z432325@unsw.edu.au',
                'name_first': 'Name1',
                'name_last': 'Lastname1',
                'handle_str': 'name1lastname1',
            },
        ],
    }
    channel_join_v1(user_id2, channel_id['channel_id'])
    assert channel_details_v1(user_id2, channel_id['channel_id']) == expected_outcome

def test_successfully_joined_channel2(clear_store, create_user, create_user2, create_user3):
    user_id = create_user
    user_id2 = create_user2
    user_id3 = create_user3
    channel_id = channels_create_v1(user_id, 'test2', True)
    channel_join_v1(user_id2, channel_id['channel_id']) 
    channel_join_v1(user_id3, channel_id['channel_id']) 
    assert channel_details_v1(user_id3, channel_id['channel_id']) == {
        'name': 'test2',
        'owner_members': [
            {
                'u_id': user_id,
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            }
        ],
        'all_members': [
            {
                'u_id': user_id,
                'email': 'z432324@unsw.edu.au',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
            },
            {
                'u_id': user_id2,
                'email': 'z432325@unsw.edu.au',
                'name_first': 'Name1',
                'name_last': 'Lastname1',
                'handle_str': 'name1lastname1',
            },            {
                'u_id': user_id3,
                'email': 'z432326@unsw.edu.au',
                'name_first': 'Name2',
                'name_last': 'Lastname2',
                'handle_str': 'name2lastname2',
            },
        ],
    }

def test_channel_doesnt_exist(clear_store, create_user, create_user2):
    user_id = create_user
    with pytest.raises(InputError):
        channel_join_v1(user_id, 0)    

def test_user_already_in_channel(clear_store, create_user, create_user2):
    user_id = create_user
    channels = channels_create_v1(user_id, 'test2', True)
    with pytest.raises(InputError):
        channel_join_v1(user_id, channels['channel_id'])

def test_list_and_join(clear_store):
    auth_user_1 = auth_register_v1("example@gmail.com","hello123", "Hayden", "Jacobs")['auth_user_id']
    auth_user_2 = auth_register_v1("exampleabc@gmail.com","hello123", "John", "Jacobs")['auth_user_id']

    channel_id1 = channels_create_v1(auth_user_1, "My Channel", True)['channel_id']

    assert channels_list_v1(auth_user_1) == {'channels': [{'channel_id': channel_id1,'name': 'My Channel'}]}
    assert channels_listall_v1(auth_user_2) == channels_list_v1(auth_user_1)
    assert channels_list_v1(auth_user_2) == {'channels': []}
    channel_join_v1(auth_user_2, channel_id1)
    assert channels_list_v1(auth_user_2) == {'channels': [{'channel_id': channel_id1,'name': 'My Channel'}]}

def test_global_owner_join_private(clear_store):
    global_owner_id = auth_register_v1("example@gmail.com","hello123", "Hayden", "Jacobs")['auth_user_id']
    normal_id = auth_register_v1("exampleemail@gmail.com","hello123", "Jake", "Pola")['auth_user_id']
    normal_id2 = auth_register_v1("sneaky@gmail.com", "38d9hja&**&", "Fake", "Name")['auth_user_id']

    channel_1 = channels_create_v1(normal_id, "Secret Channel", False)['channel_id']
    #  Test normal member cant get in
    with pytest.raises(AccessError):
        channel_join_v1(normal_id2, channel_1)

    # Verify owner is not in the channel    
    assert channels_list_v1(global_owner_id) == {'channels': []}

    channel_join_v1(global_owner_id, channel_1)

    assert channels_list_v1(global_owner_id) == {'channels': [{'channel_id': channel_1, 'name': 'Secret Channel'}]}

def test_fake_id(clear_store, create_user):
    user_id = create_user
    fake_id = user_id + 1
    channel_1 = channels_create_v1(user_id, "New Channel", True)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(fake_id, channel_1)
