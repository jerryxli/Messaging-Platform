"""
These tests were written purely from the spec and stubbed functions and are a check on the code 

"""
import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_details_v1, channel_join_v1, channel_messages_v1, channel_invite_v1
from src.error import AccessError
from src.other import clear_v1

@pytest.fixture
def clear_state():
    clear_v1()



def test_scenario_1(clear_state):
    auth_user_1 = auth_register_v1("example@gmail.com","hello123", "Hayden", "Jacobs")['auth_user_id']
    channel_created = channels_create_v1(auth_user_1, "Hayden", False)['channel_id']
    assert channel_details_v1(auth_user_1, channel_created) ==  {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': auth_user_1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': auth_user_1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }


def test_6_3_spec_Access_Errors(clear_state):
    auth_user_1 = auth_register_v1("example@gmail.com","hello123", "Hayden", "Jacobs")['auth_user_id']
    # Since there is only one user and the ids must be unique this is a fake user
    fake_auth = auth_user_1 + 1
    # Access error testing

    with pytest.raises(AccessError):
        channels_create_v1(fake_auth, "New Channel", False)

    with pytest.raises(AccessError):
        channels_list_v1(fake_auth)

    with pytest.raises(AccessError):
        channels_listall_v1(fake_auth)
    
    channel_1 = channels_create_v1(auth_user_1, "Cool channel", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(fake_auth, channel_1)

    with pytest.raises(AccessError):
        channel_messages_v1(fake_auth, channel_1, 0)
    
    with pytest.raises(AccessError):
        channel_join_v1(fake_auth, channel_1)
    
  #  with pytest.raises(AccessError):
  #      channel_invite_v1(fake_auth, channel_1, auth_user_1)





