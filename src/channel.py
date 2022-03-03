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

# check if the user is already in the channel
def check_user_in_channel(user_id, channel):
    if user_id in channel['channel_members']:
        return True
    else:
        return False
    
def channel_messages_v1(auth_user_id, channel_id, start):
    start = int(start)
    page_threshold = 50
    store = data_store.get()

    user = None
    users = store['users']
    if auth_user_id in users.keys():
        user = users[auth_user_id]

    channel = None
    channels = store['channels']
    if channel_id in channels.keys():
        channel = channels[channel_id]

    if channel == None:
        raise InputError("channel_id does not refer to a valid channel")
    if check_user_in_channel(auth_user_id, channel) == False:
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")
    
    # determine if start is greater than total number of messages, if so, return InputError
    if start > len(channel['messages']):
        raise InputError("start is greater than the total number of messages in the channel")

    messages = []
    not_displayed = list(reversed(channel['messages']))[start:]
    end = -1 if len(messages) == len(not_displayed) else start + page_threshold
    return {'messages': messages, 'start': start, 'end': end}

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
    


