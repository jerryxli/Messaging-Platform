"""
Channel
Filename: channel.py

Author: Tetian Madfouni (z5361722), Jacqueline Chen (z5360310), Leo Shi (z5364321),
Samuel Bell (z5362604), Jerry Li (z5362290)
Created: 22.02.2022

Description: Allows the user to invite a user to a channel, get the details of a channel,
get information of the messages within a channel and join a channel.
"""
from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import verify_user, is_global_user

GLOBAL_PERMISSION_OWNER = 2
PAGE_THRESHOLD = 50

def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    Invites a user to join a channel.

    Exceptions:
        AccessError     - Occurs when auth_user_id is invalid
        AccessError     - Occurs when auth_user_id is not a member of the channel
        InputError      - Occurs when u_id is already a member of the channel
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when u_id is invalid

    Arguments:
        auth_user_id (int)  - The id of the user
        u_id (int)          - The id of the invited user
        channel_id (int)    - The id of the channel

    Return Value:
        None
    """
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

    if check_user_in_channel(u_id, channel):
        raise InputError("u_id refers to a user who is already a member of the channel")
    if not check_user_in_channel(auth_user_id, channel):
        raise AccessError

    altered_users = {k: non_password_global_permission_field(v) for k,v in users.items()}
    for user_id, user in altered_users.items():
        user['u_id'] = user_id
        channel['all_members'].append(altered_users[u_id])

    data_store.set(store)


def channel_details_v1(auth_user_id:int, channel_id:int)->dict:
    """
    Returns assosciated details of a channel.

    Exceptions:
        AccessError     - Occurs when auth_user_id is invalid
        AccessError     - Occurs when auth_user_id is not a member of the channel
        InputError      - Occurs when channel_id is invalid

    Arguments:
        auth_user_id (int)  - The id of the user
        channel_id (int)    - The id of the channel

    Return Value:
        Returns { name: , is_public: , owner_members: [], all_members: [], }
        on successful creation
    """
    store = data_store.get()
    channels = store['channels']

    # Checks for Input error: when the channel_id does not exist
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError
    ids = [user['u_id'] for user in channel['all_members']]
    # Checks for Access error: when the user is not a member of the channel
    if auth_user_id in ids:
        return {k: v for k, v in channel.items() if k not in ['messages']}
    else:
        raise AccessError("User is not a member of the channel")


def channel_messages_v1(auth_user_id:int, channel_id:int, start:int)->dict:
    """
    Returns up to 50 messages between the start index and start + 50.

    Exceptions:
        AccessError     - Occurs when auth_user_id is invalid
        AccessError     - Occurs when auth_user_id is not a member of the channel
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when start is greater than the total number of messages

    Arguments:
        auth_user_id (int)  - The id of the user
        channel_id (int)    - The id of the channel
        start (int)         - The start index

    Return Value:
        Returns { messages, start, end } on successful creation
    """
    store = data_store.get()
    channels = store['channels']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError('channel_id does not refer to a valid channel')
    if not check_user_in_channel(auth_user_id, channel):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")

    # determine if start is greater than total number of messages, if so, return InputError
    if start > len(channel['messages']):
        raise InputError("start is greater than the total number of messages in the channel")

    messages = []
    not_displayed = list(reversed(channel['messages']))[start:]
    messages.extend(not_displayed[:min(PAGE_THRESHOLD, len(not_displayed))])
    
    end = -1 if len(messages) == len(not_displayed) else start + PAGE_THRESHOLD
    return {'messages': messages, 'start': start, 'end': end}


def check_user_in_channel(auth_user_id:int, channel:dict)->bool:
    """
    Checks whether a user is in a channel or not

    Arguments:
        user_id (int)   - the id of the user
        channel (dict)  - the channel to check

    Returns:
        A boolean, true if the user is in the channel, false if not
    """
    ids = [user['u_id'] for user in channel['all_members']]
    return bool(auth_user_id in ids)


def channel_join_v1(auth_user_id:int, channel_id:int)->None:
    """
    Adds a new user to a channel provided it is public and they aren't already in it

    Exceptions:
        AccessError     - Occurs when auth_user_id is invalid
        AccessError     - Occurs when auth_user_id is not a member of the channel
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when auth_user_id is already a member of the channel

    Arguments:
        auth_user_id (int)  - the id of the user
        channel_id (int)    - the id of the channel to join

    Returns:
        None

    """
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id does not refer to a valid channel")
    # check if the channel is public
    altered_users = {k: non_password_global_permission_field(v) for k,v in users.items()}
    for user_id, user in altered_users.items():
        user['u_id'] = user_id
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


def channel_leave_v1(auth_user_id:int, channel_id:int)->None:
    """
    This function allows a user to leave a channel

    Exceptions:
        AccessError     - Occurs when the user_id is invalid
        AccessError     - Occurs when the user is not a member of the channel
        InputError      - Occurs when the channel_id is invalid

    Arguments: 
        auth_user_id (int)      - User id
        channel_id (int)        - Channel id

    Returns:
        None         
    """
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    # Check channel_id is valid
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("Channel id not valid")
        
    # Check auth_user_id is in channel
    user = non_password_global_permission_field(users[auth_user_id])
    user['u_id'] = auth_user_id
    user['handle_str'] = user.pop('handle')
    if user in channel['owner_members']:
        channel['owner_members'].remove(user)
        channel['all_members'].remove(user)
    elif user in channel['all_members']:
        channel['all_members'].remove(user)
    else:
        raise AccessError("User not in channel")
    
    data_store.set(store)     

def channel_addowner_v1(auth_user_id:int, channel_id:int, u_id:int)->None:
    """
    This function makes the user with u_id an owner of the channel

    Exceptions:
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when u_id is invalid
        InputError      - Occurs when u_id is not a member
        InputError      - Occurs when u_id is already an owner
        AccessError     - Occurs when auth_user_id does not have owner permissions
    
    Arguments:
        auth_user_id (int)      - Authorised user id
        channel_id (int)        - Channel id
        u_id (int)              - User id 

    Returns:
        None
    """
    if not verify_user(u_id):
        raise InputError("U id not valid")
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("Channel id not valid")

    # Check if auth_user is a member of the channel
    if not check_user_in_channel(auth_user_id, channel):
        raise AccessError("Auth_user_id does not have owner permissions")

    # Check if auth_user has owner permissions
    owner_members = channel['owner_members']
    auth_user = users[auth_user_id]
    if not auth_user['global_permission'] == GLOBAL_PERMISSION_OWNER:
        altered_auth = non_password_global_permission_field(users[auth_user_id])
        altered_auth['u_id'] = auth_user_id
        altered_auth['handle_str'] = altered_auth.pop('handle')
        if altered_auth not in owner_members:
            raise AccessError("Auth_user_id does not have owner permissions")
    
    # Check if u_id is a member of the channel
    if not check_user_in_channel(u_id, channel):
        raise InputError("U_id not a member")
    
    altered_user = non_password_global_permission_field(users[u_id])
    altered_user['u_id'] = u_id
    altered_user['handle_str'] = altered_user.pop('handle')

    # Check if user is already an owner, otherwise add to list of owners
    if altered_user not in owner_members:
        owner_members.append(altered_user)
    else:
        raise InputError("User_id is already an owner")

    data_store.set(store)

def channel_removeowner_v1(auth_user_id:int, channel_id:int, u_id:int)->None:
    """
    Removes the owner with user id u_id

    Exceptions:
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when u_id is invalid
        InputError      - Occurs when u_id is not an owner
        InputError      - Occurs when u_id is the only owner
        AccessError     - Occurs when channel_id does not have owner permissions

    Arguments:
        auth_user_id (int)  - the id of the user
        channel_id (int)    - the id of the channel
        u_id (int)          - the id of the owner 

    Returns:
        None
    """
    if not verify_user(u_id):
        raise InputError("U id not valid")
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("Channel id not valid")

    # Check the auth_user and u_id are members of the channel first
    if not check_user_in_channel(u_id, channel):
        raise InputError("U_id not a member")

    # Check if auth_user has owner permissions
    owner_members = channel['owner_members']
    auth_user = users[auth_user_id]
    if not auth_user['global_permission'] == GLOBAL_PERMISSION_OWNER:
        altered_auth = non_password_global_permission_field(users[auth_user_id])
        altered_auth['u_id'] = auth_user_id
        altered_auth['handle_str'] = altered_auth.pop('handle')
        if altered_auth not in owner_members:
            raise AccessError("Auth_user_id does not have owner permissions")
    altered_user = non_password_global_permission_field(users[u_id])
    altered_user['u_id'] = u_id
    altered_user['handle_str'] = altered_user.pop('handle')

    # Check if user is only owner, otherwise remove from list of owners
    if len(owner_members) != 1 and altered_user in owner_members:
        owner_members.remove(altered_user)
    else:
        raise InputError("User_id is the only owner")
    data_store.set(store)


def non_password_global_permission_field(user:dict)->dict:
    """
    Removes all non-password fields from a user to print them

    Arguments:
        user (dict) - dictionary of all user details

    Returns:
        Dictionary with password field removed

    """
    user = {k: v for k,v in user.items() if k not in ['password', 'global_permission', 'sessions']}
    return user

def is_valid_channel(channel_id:int)->bool:
    """
    Checks if the channel_id is valid

    Arguments:
        channel_id (int) - the channel id

    Returns:
        True if the channel_id is valid, False otherwise
    """
    store = data_store.get()
    channels = store['channels']
    if channel_id in channels:
        return True
    else:
        return False