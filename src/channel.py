from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

# given a channel id, return a channel dictionary
def get_channel(id):
    store = data_store.get()
    channels = store['channels']
    for channel in channels:
        if int(id) == channel['channel_id']:
            return channel
    return None

# check if the user is already in the channel
def check_user_in_channel(user_id, channel):
    for member in channel['channel_members']:
        if user_id == member:
            return True
    return False

def channel_join_v1(auth_user_id, channel_id):
    channel = get_channel(channel_id)
    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    # check if the channel is public
    if channel['is_public']:
        # check if the user is already in the channel
        check_for_user = check_user_in_channel(auth_user_id, channel)
        if check_for_user:
            raise InputError("the authorised user is already a member of the channel")
        
        # channel is public and user isn't in the channel yet. Add to channel
        channel['channel_members'].append(auth_user_id)
    else:
        raise(AccessError)

