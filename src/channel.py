from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    channel = get_channel(channel_id)
    if #auth_user_id is invalid
        raise(AccessError) 
    if #u_id is invalid user
        raise InputError("u_id does not refer to a valid user")
    if check_user_in_channel(u_id, channel) == True:
        raise InputError("u_id reders to a user who is already a member of the channel")
    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    elif check_user_in_channel(auth_user_id, channel) == False:
        raise(AccessError)

    channel_join_v1(u_id, channel_id)
    

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
    
