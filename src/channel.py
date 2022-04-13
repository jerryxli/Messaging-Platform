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
from time import time
import src.other as other
import threading


def channel_invite_v2(auth_user_id, channel_id, u_id):
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
    if other.verify_user(u_id) is False:
        raise InputError(description="u_id does not refer to a valid user")

    store = data_store.get()
    channel = None
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError(description="channel_id does not refer to a valid channel")

    if other.check_user_in_channel(u_id, channel):
        raise InputError(description="u_id refers to a user who is already a member of the channel")
    if not other.check_user_in_channel(auth_user_id, channel):
        raise AccessError(description="User issuing invite is not part of channel")

    altered_users = {k: other.non_password_global_permission_field(v) for k,v in users.items()}
    for user_id, user in altered_users.items():
        user['u_id'] = user_id
        user['handle_str'] = user.pop('handle')
        channel['all_members'].append(altered_users[u_id])

    data_store.set(store)


def channel_details_v2(auth_user_id:int, channel_id:int)->dict:
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

    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError(description="channel_id does not refer to a valid channel")
    ids = [user['u_id'] for user in channel['all_members']]
    
    if auth_user_id in ids:
        return {k: v for k, v in channel.items() if k not in ['messages']}
    else:
        raise AccessError(description="User is not a member of the channel")


def channel_messages_v2(auth_user_id:int, channel_id:int, start:int)->dict:
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
    stored_messages = store['messages']
    if channel_id in channels:
        channel = channels[channel_id]
    else:
        raise InputError(description='channel_id does not refer to a valid channel')
    if not other.check_user_in_channel(auth_user_id, channel):
        raise AccessError(description="User is not a member of the channel")
    channel_messages = []
    for message in stored_messages.values():
        if message['is_channel'] == True and message['id'] == channel_id:
            channel_messages.append({'message': message['message'], 'message_id': message['message_id'], 'u_id': message['u_id'], 'time_sent': message['time_sent']})
    if start > len(channel_messages):
        raise InputError(description="start is greater than the total number of messages in the channel")
    messages = []
    not_displayed = list(reversed(channel_messages))[start:]
    messages.extend(not_displayed[:min(other.PAGE_THRESHOLD, len(not_displayed))])

    end = -1 if len(messages) == len(not_displayed) else start + other.PAGE_THRESHOLD
    return {'messages': messages, 'start': start, 'end': end}




def channel_join_v2(auth_user_id:int, channel_id:int)->None:
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

    altered_users = {k: other.non_password_global_permission_field(v) for k,v in users.items()}
    for user_id, user in altered_users.items():
        user['u_id'] = user_id
        user['handle_str'] = user.pop('handle')
    if channel['is_public'] or (not channel['is_public'] and other.is_global_user(auth_user_id)):
        if other.check_user_in_channel(auth_user_id, channel):
            raise InputError("the authorised user is already a member of the channel")
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

    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("Channel id not valid")
        
    user = other.non_password_global_permission_field(users[auth_user_id])
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
    if not other.verify_user(u_id):
        raise InputError("U id not valid")
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("Channel id not valid")

    if not other.check_user_in_channel(auth_user_id, channel):
        raise AccessError("Auth_user_id does not have owner permissions")

    owner_members = channel['owner_members']
    auth_user = users[auth_user_id]
    if not auth_user['global_permission'] == other.GLOBAL_PERMISSION_OWNER:
        altered_auth = other.non_password_global_permission_field(users[auth_user_id])
        altered_auth['u_id'] = auth_user_id
        altered_auth['handle_str'] = altered_auth.pop('handle')
        if altered_auth not in owner_members:
            raise AccessError("Auth_user_id does not have owner permissions")
    
    if not other.check_user_in_channel(u_id, channel):
        raise InputError("U_id not a member")
    
    altered_user = other.non_password_global_permission_field(users[u_id])
    altered_user['u_id'] = u_id
    altered_user['handle_str'] = altered_user.pop('handle')

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
    if not other.verify_user(u_id):
        raise InputError("U id not valid")
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError("channel_id not valid")
    owner_members = [user['u_id'] for user in channel['owner_members']]
    
    if not other.check_user_in_channel(auth_user_id, channel):
        raise AccessError("Auth_user_id does not have owner permissions")

    if u_id not in owner_members:
        raise InputError(description="u_id is not an owner of channel")
    
    if not users[auth_user_id]['global_permission'] == other.GLOBAL_PERMISSION_OWNER and not auth_user_id in owner_members:
        raise AccessError(description='auth_user_id does not have owner permissions')
    if len(owner_members) == 1:
        raise InputError(description="u_id is the only owner")
    user_index = owner_members.index(u_id)
    channel['owner_members'].pop(user_index)
    channels[channel_id] = channel
    store['channels'] = channels
    data_store.set(store)

def print_standup(auth_user_id:int, channel:dict,  channel_id:int):
    #print standup messages
    store = data_store.get()
    messages = store['messages']
    new_message_id = len(messages)
    messages[new_message_id] = {'message_id': new_message_id, 'u_id': auth_user_id, 'message': channel['standup_messages'], 'time_sent': time(), 'is_channel': True, 'id': channel_id}
    #then clear standup_messages and set standup_active to false
    channel['standup_messages'] = ''
    channel['standup_active'] = False


def standup_start_v1(auth_user_id:int, channel_id:int, length:int):
    """
    Starts the standup period for 'length' seconds.  

    Exceptions:
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when length is a negative integer
        InputError      - Occurs when an active standup is already running
        AcessError      - Occurs when the auth user is not a member of the channel

    Arguments:
        auth_user_id (int)  - the id of the user
        channel_id (int)    - the id of the channel
        length (int)        - the length of the standup

    Returns:
        Returns {time_finish} on successful creation
    """
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    if length < 0:
        raise InputError(description="Length is negative")

    if channel_id in channels.keys():
        channel = channels[channel_id]
    else:
        raise InputError(description="Channel id not valid")
        
    user = other.non_password_global_permission_field(users[auth_user_id])
    user['u_id'] = auth_user_id
    user['handle_str'] = user.pop('handle')
    if user in channel['all_members']:
        channel['standup_active'] = True
        # create thread here
        standup_thread = threading.Timer(length, print_standup, args = (auth_user_id, channel, channel_id))
        standup_thread.start()
    else:
        raise AccessError(description="User is not a member of channel")
    
    data_store.set(store)
    return time.time() + length