from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import verify_user, is_global_user

PAGE_THRESHOLD = 50

def check_user_in_channel(auth_user_id:int, channel:dict)->bool:
    '''
    Checks whether a user is in a channel or not

    Arguments:
        user_id (int) - the id of the user
        channel (dict) - the channel to check

    Returns:
        A boolean, true if the user is in the channel, false if not

    '''
    ids = [user['u_id'] for user in channel['channel_members']]
    return bool(auth_user_id in ids)

def channel_invite_v1(auth_user_id, channel_id, u_id):
    if verify_user(auth_user_id) is False:
        raise(AccessError)
    if verify_user(u_id) is False:
        raise InputError("u_id does not refer to a valid user")

    store = data_store.get()
    channel = None
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")

    if check_user_in_channel(u_id, channel) == True:
        raise InputError("u_id refers to a user who is already a member of the channel")
    if check_user_in_channel(auth_user_id, channel) == False:
        raise(AccessError)

    altered_users = {k: non_password_global_permission_field(v) for k,v in users.items()}
    for id, user in altered_users.items():
        user['u_id'] = id
        channel['channel_members'].append(altered_users[u_id])

    data_store.set(store) 

def channel_details_v1(auth_user_id:int, channel_id:int)->dict:
    """
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
    """
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
    ids = [user['u_id'] for user in channel['all_members']]
    # Checks for Access error: when the user is not a member of the channel
    if auth_user_id in ids:
        return {k: v for k, v in channel.items() if k not in ['is_public', 'messages']}
    else:
        raise AccessError
    return channel_details
    
def channel_messages_v1(auth_user_id:int, channel_id:int, start:int)->dict:
    store = data_store.get()
    user = None
    users = store['users']

    if not verify_user(auth_user_id):
        raise AccessError("Auth id not valid")

    if auth_user_id in users.keys():
        user = users[auth_user_id]
    else:
        raise InputError('Invalid auth_user_id')
    channels = store['channels']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError('channel_id does not refer to a valid channel')
    if check_user_in_channel(auth_user_id, channel) == False:
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")
    
    # determine if start is greater than total number of messages, if so, return InputError
    if start > len(channel['messages']):
        raise InputError("start is greater than the total number of messages in the channel")

    messages = []
    not_displayed = list(reversed(channel['messages']))[start:]
    end = -1 if len(messages) == len(not_displayed) else start + PAGE_THRESHOLD
    return {'messages': messages, 'start': start, 'end': end}


def check_user_in_channel(auth_user_id:int, channel:dict)->bool:
    """
    Checks whether a user is in a channel or not

    Arguments:
        user_id (int) - the id of the user
        channel (dict) - the channel to check
    
    Returns:
        A boolean, true if the user is in the channel, false if not
    """
    ids = [user['u_id'] for user in channel['all_members']]
    return bool(auth_user_id in ids)


def channel_join_v1(auth_user_id:int, channel_id:int)->None:
    """
    Adds a new user to a channel provided it is public and they aren't already in it

    Arguments:
        auth_user_id (int) - the id of the user
        channel_id (int) - the id of the channel to join
    
    Returns:
        None

    """
    if not verify_user(auth_user_id):
        raise AccessError("Auth id not valid")
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")
    # check if the channel is public
    altered_users = {k: non_password_global_permission_field(v) for k,v in users.items()}
    for id, user in altered_users.items():
        user['u_id'] = id
        user['handle_str'] = user.pop('handle')
    if channel['is_public'] or (not channel['is_public'] and is_global_user(auth_user_id)):
        # check if the user is already in the channel
        if check_user_in_channel(auth_user_id, channel):
            raise InputError("the authorised user is already a member of the channel")
        # channel is public and user isn't in the channel yet. Add to channel
        channel['all_members'].append(altered_users[auth_user_id])
    else:
        raise AccessError
    
    data_store.set(store)
    
def non_password_global_permission_field(user:dict)->dict:
    """
    Removes all non-password fields from a user to print them

    Arguments:
        user (dict) - dictionary of all user details
    
    Returns:
        Dictionary with password field removed
    
    """
    user = {k: v for k,v in user.items() if k not in ['password', 'global_permission']}
    return user


