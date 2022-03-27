"""
Dm
Filename: dm.py

Author: Jacqueline Chen (z5360310), Jerry Li (z5362290), Tetian Madfouni (z5361722)
Created: 22.03.2022

Description: Allows the user to create a dm, list dms, leave dms,
message in a dm, get details of a dm, and remove a dm.
"""
from time import time
from src.data_store import data_store
from src.channel import non_password_global_permission_field
from src.error import InputError, AccessError
from src.other import verify_user

PAGE_THRESHOLD = 50

def dm_create_v1(auth_user_id:int, u_ids:list)->dict:
    """
    Creates a dm between the auth_user_id and the user(s) in the u_ids dict

    Exceptions:
        InputError          - Occurs when any u_id is invalid
        InputError          - Occurs when duplicate u_id occurs

    Arguments:
        auth_user_id (int)  - The id of the user
        u_ids (list)        - List of u_ids to add to the dm

    Return Value:
        Returns { 'dm_id' } on successful creation
    """
    store = data_store.get()
    dms = store['dms']
    users = store['users']

    # U_id is not valid
    if len(u_ids) != 0:
        if any(verify_user(u_id) for u_id in u_ids) == False:
            raise InputError(description = "U_id not valid")

    # Check for duplicate u_id
    user_set = set(u_ids)
    if len(user_set) < len(u_ids):
        raise InputError(description = "Duplicate u_ids entered")
    if auth_user_id not in u_ids:
        u_ids.append(auth_user_id)

    # Create users list with user info
    members = []
    for id in u_ids:
        user = non_password_global_permission_field(users[id])
        user['u_id'] = id
        user['handle_str'] = user.pop('handle')
        members.append(user) 

    # Create name
    name = ''
    user_handles = []
    for id in u_ids:
        user_handles.append(users[id]['handle'])
    user_handles.sort()
    name = ', '.join(user_handles)

    # Information for the dm
    dm_info = {}
    dm_id = len(dms)
    dm_info['creator'] = auth_user_id
    dm_info['name'] = name
    dm_info['members'] = members
    dm_info['messages'] = []
    dms[dm_id] = dm_info
    store['dms'] = dms
    data_store.set(store)
    
    return {'dm_id': dm_id}

def dm_list_v1(auth_user_id:int)->dict:
    """
    Lists all dms auth_user_id is apart of

    Exceptions:

    Arguments:
        auth_user_id (int)  - The id of the user

    Return Value:
        Returns { 'dms' } upon successful creation 
        in format {'dms': [{'dm_id': int, 'name': str}] } 
    """
    store = data_store.get()
    dms = store['dms']
    dm_list = []
    for key, value in dms.items():
        ids = [user['u_id'] for user in value['members']]
        if auth_user_id in ids:
            dm_list.append({'name': value['name'], 'dm_id': key})

    return { 'dms': dm_list }


    # return { 'dms': [{'dm_id': key, 'name': dm['name']}] 
    #         for key, dm in dms.items()}



def dm_remove_v1(auth_user_id:int, dm_id:int)->None:
    """
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Exceptions:

    Arguments:
        auth_user_id (int)  - The id of the user
        dm_id (int)         - The id of the dm

    Return Value:
        None
    """

    store = data_store.get()
    dms = store['dms']
    users = store['users']
    if dm_id not in dms:
        raise InputError(description = "dm_id is not valid")
    dm = dms[dm_id]
    user = non_password_global_permission_field(users[auth_user_id])
    user['u_id'] = auth_user_id
    user['handle_str'] = user.pop('handle')
    if auth_user_id == dm['creator']: # dm['owner_members']
        # remove DM
        del dms[dm_id]
    elif user in dm['members']:
        raise AccessError(description = "User is not the original DM creator")
    else:
        raise AccessError(description = "User is not in DM")

    store['dms'] = dms
    data_store.set(store)
    return
    


def dm_details_v1(auth_user_id:int, dm_id:int)->dict:
    """
    Returns details of the dm in a dict

    Exceptions:

    Arguments:
        auth_user_id (int)  - The id of the user
        dm_id (int)         - The id of the dm

    Return Value:
        Returns { 'name', 'members' } upon successful creation
    """
    store = data_store.get()
    dms = store['dms']

    if dm_id in dms.keys():
        dm = dms[dm_id]
    else:
        raise InputError(description = "Dm_id not valid")

    dm_details = {}
    member_ids = [member['u_id'] for member in dm['members']]

    if auth_user_id in member_ids:
        dm_details['name'] = dm['name']
        dm_details['members'] = dm['members']
    else:
        raise AccessError(description = "Auth_user_id not a member")

    data_store.set(store)
    return dm_details


def dm_leave_v1(auth_user_id:int, dm_id:int)->None:
    """
    Removes auth_user_id from dm of dm_id

    Exceptions:

    Arguments:
        auth_user_id (int)      - The id of the user
        dm_id (int)             - The id of the dm

    Return Value:
        None
    """
    store = data_store.get()
    dms = store['dms']
    users = store['users']

    if dm_id in dms.keys():
        dm = dms[dm_id]
    else:
        raise InputError(description = "Dm_id not valid")

    user = non_password_global_permission_field(users[auth_user_id])
    user['u_id'] = auth_user_id
    user['handle_str'] = user.pop('handle')
    if dm['creator'] == auth_user_id:
        # user is owner of channel
        dm['creator'] = None
        dm['members'].remove(user)
    elif user in dm['members']:
        dm['members'].remove(user)
    else:
        raise AccessError(description = "User is not in DM")

    store['dms'] = dms
    data_store.set(store)
    return

def dm_send_v1(auth_user_id:int, message:str, dm_id:int)->dict:
    """
    Allows a user to send a message in the specified DM

    Arguments:
        auth_user_id (int) - The user id of the sender
        message (str)      - The message to be sent
        dm_id (int)        - The id of the DM where the message will be sent to

    Errors
        AccessError        - Where the user does not belong to the specified DM
        InputError         - Where the DM id is invalid or the message is not between 1 and 1000 characters
    
    Return Value:
        Dictionary containing message_id, on success
    """
    store = data_store.get()
    dms = store['dms']
    if dm_id not in dms:
        raise InputError(description="dm_id is invalid")
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description="Invalid message length")
    dm = dms[dm_id]
    u_ids = [user['u_id'] for user in dm['members']]
    if auth_user_id not in u_ids:
        raise AccessError(description="User is not part of DM")
    message_id = store['messages']
    dm['messages'].append({'message_id': message_id, 'u_id': auth_user_id, 'message': message, 'time_sent': time()})
    store['messages'] += 1
    dms[dm_id] = dm
    store['dms'] = dms
    data_store.set(store)
    return {'message_id': message_id}


def dm_messages_v1(auth_user_id:int, dm_id:int, start:int)->dict:
    """
    Returns the messages of a dm from start index + 50

    Exceptions:

    Arguments:
        auth_user_id (int)      - The id of the user
        dm_id (int)             - The id of the dm
        start (int)             - The start index

    Return Value:
        Returns { 'messages', 'start', 'end' } upon successful creation
    """
    store = data_store.get()
    dms = store['dms']
    if dm_id in dms:
        dm = dms[dm_id]
    else:
        raise InputError(description = 'dm_id does not refer to a valid channel')
    u_ids = [user['u_id'] for user in dm['members']]
    if auth_user_id not in u_ids:
        raise AccessError(description = "dm_id is valid but user is not a member of the channel")
    if start > len(dm['messages']):
        raise InputError(description = "Start is greater than the total number of messages in channel")
    messages = []
    not_displayed = list(reversed(dm['messages']))[start:]
    messages.extend(not_displayed[:min(PAGE_THRESHOLD, len(not_displayed))])
    end = -1 if len(messages) == len(not_displayed) else start + PAGE_THRESHOLD
    return {'messages': messages, 'start': start, 'end': end}