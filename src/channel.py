from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import verify_user

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    '''
    When a auth_user_id and channel_id is passed in, the details for the channel is returned.

    Exceptions:
        AccessError when auth_user_id is invalid.
        AccessError when auth_user_id is not a member in the channel.
        InputError when channel_id is invalid.
    
    Arguments: 
        int auth_user_id, int channel_id
        
    Return Value:
        The details of a channel in the format:
        { name: , is_public: , owner_members: [], all_members: [], }
    '''
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    # Checks for when the auth_user_id is not registered
    if verify_user(auth_user_id) == False:
        raise(AccessError)
    # Checks for Input error: when the channel_id does not exist
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError
    ids = []
    for user in channel['channel_members']:
        print(user)
        ids.append(user['u_id'])
    # Checks for Access error: when the user is not a member of the channel
    if auth_user_id in ids:
        # Create a blank dictionary that will contain the channel details
        channel_details = {}

        # Add the details into the channel_details dictionary
        channel_details['name'] = channel['name']
        channel_details['is_public'] = channel['is_public']
        channel_details['owner_members'] = channel['channel_owners']
        channel_details['all_members'] = channel['channel_members']
    else:
        raise AccessError
    return channel_details

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

def check_user_in_channel(auth_user_id, channel):
    ids = [user['u_id'] for user in channel['channel_members']]
    if auth_user_id in ids:
        return True
    else:
        return False


def channel_join_v1(auth_user_id, channel_id):
    channel = None
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")
    # check if the channel is public
    ignore_keys = ['password']
    altered_users = users
    for k,v in altered_users.items():
        fresh = {}
        for key, item in v.items():
            if key not in ignore_keys:
                fresh[key] = item
        fresh['u_id'] = auth_user_id
        altered_users[k] = fresh
    if channel['is_public']:
        # check if the user is already in the channel
        if check_user_in_channel(auth_user_id, channel):
            raise InputError("the authorised user is already a member of the channel")
        # channel is public and user isn't in the channel yet. Add to channel
        channel['channel_members'].append(altered_users[auth_user_id])
    else:
        raise(AccessError)
    
    data_store.set(store)
    


