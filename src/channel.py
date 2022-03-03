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
    start = int(start)
    page_threshold = 50

    # locate user_id, if not found, return AccessError
    user = None
    store = data_store.get()
    users = store['users']
    if auth_user_id in users.keys():
        user = users[user_id]
    else:
        raise AccessError("channel_id is valid and the authorised user is not a memeber of the channel")
    # locate channel_id, if not found, return InputError
    channel = None
    channels = store['channels']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")
    # determine if start is greater than total number of messages, if so, return InputError
    if start > len(channel['messages']):
        raise InputError("start is greater than the total number of messages in the channel")

    messages = []
    not_displayed = list(reversed(channel['messages']))[start:]
    end = -1 if len(messages) == len(not_displayed) else start + page_threshold

    return {'messages': messages, 'start': start, 'end': end}


# check if the user is already in the channel
def check_user_in_channel(user_id, channel):
    if user_id in channel['channel_members']:
        return True
    else:
        return False

def channel_join_v1(auth_user_id, channel_id):
    channel = None
    store = data_store.get()
    channels = store['channels']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")
    # check if the channel is public
    if channel['is_public']:
        # check if the user is already in the channel
        if check_user_in_channel(auth_user_id, channel):
            raise InputError("the authorised user is already a member of the channel")
        # channel is public and user isn't in the channel yet. Add to channel
        channel['channel_members'].append(auth_user_id)
    else:
        raise(AccessError)
    
    data_store.set(store)
    


