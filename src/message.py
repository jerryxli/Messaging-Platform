"""
Message
Filename: message.py

Author: Tetian Madfouni (z5361722), Jacqueline Chen (z5360310), Leo Shi (z5364321),
Samuel Bell (z5362604), Jerry Li (z5362290)
Created: 19.03.2022

Description: Allows the user to send, edit and remove messages.
"""
from time import time

from src.data_store import data_store
from src.error import InputError, AccessError
from src.channel import check_user_in_channel

def message_send_v1(user_id, channel_id, message):
    """
    Send a message from the authorised user to the channel specified by channel_id

    Exceptions:
        AccessError     - Occurs when channel_id is valid and the user is not a member of the channel
        InputError      - Occurs when channel_id is invalid
        InputError      - Occurs when the length of a message is < 1 or > 1000 characters

    Arguments:
        user_id (int)       - The token of the user
        channel_id (int)    - The id of the channel
        message (string)    - The message

    Return Value:
        Returns { message_id } when successful
    """
    store = data_store.get()
    channels = store['channels']

    if channel_id in channels.keys():
        message_channel = channels[channel_id]
    else:
        raise InputError(description = "channel_id does not refer to a valid channel")
        
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description = "Length of message is less than 1 or over 1000 characters")

    if check_user_in_channel(user_id, message_channel):
        new_message_id = store['messages']
        message_channel['messages'].append({'message_id': new_message_id, 'u_id': user_id, 'message': message, 'time_sent': time()})
        store['channels'] = channels
        store['messages'] += 1
        data_store.set(store)
        return ({'message_id': new_message_id})
    else:
        raise AccessError(description = "channel_id is valid and the user is not a member of the channel")

    
def message_edit_v1(user_id, message_id, message):
    """
    Given a message, update its text with new text. 
    If the new message is an empty string, the message is deleted.

    Exceptions:
        AccessError     - Occurs when the message_id is valid and the message was not sent by the user trying to edit
        AccessError     - Occurs when the message_id is valid and the user does not have owner permissions in the channel/DM
        InputError      - Occurs when the length of a message over 1000 characters
        InputError      - Occurs when message_id does not refer to a valid message within a channel

    Arguments:
        token (int)         - The token of the user
        message_id (int)    - The id of the message
        message (string)    - The message

    Return Value:
        Returns { } when successful
    """
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']
    message_info = get_message_and_channel(message_id)

    if message_info is None:
        raise InputError(description = "message_id does not refer to a valid message within a channel/DM that the authorised user has joined")
    print(user_id)
    if message_info['type'] == 'channel':
        u_ids = [user['u_id'] for user in channels[message_info['channel_id']]['owner_members']]
        all_u_ids = [user['u_id'] for user in channels[message_info['channel_id']]['all_members']]
        print('\n\n\n\\n\n\n\n\n\n\n', user_id in u_ids)
        if user_id not in u_ids and user_id not in all_u_ids:
            raise InputError(description = "message_id is valid but user is not in channel")
        if message_info['message']['u_id'] != user_id and user_id not in u_ids:
            raise AccessError(description = "message_id is valid but user does not have permissions to edit")

    else:
        u_ids = [user['u_id'] for user in dms[message_info['dm_id']]['members']]
        if user_id not in u_ids or message_info['message']['u_id'] != user_id:
            raise AccessError(description = "message_id is valid but user does not have permissions to edit")
    if len(message) > 1000:
        raise InputError(description = "message over 1000 characters")
    if message == '':
        message_remove_v1(user_id, message_id)
    # edit the message
    else:
        message_info['message']['message'] = message
    store['channels'] = channels
    store['dms'] = dms
    data_store.set(store)
    return {}



def message_remove_v1(user_id, message_id):
    """
    Given a message_id for a message, this message is removed from the channel/DM

    Exceptions:
        AccessError     - Occurs when the message_id is valid and the message was not sent by the user trying to edit
        AccessError     - Occurs when the message_id is valid and the user does not have owner permissions in the channel/DM
        InputError      - Occurs when message_id does not refer to a valid message within a channel/DM  
    
    Arguments:
        token (int)         - The token of the user
        message_id (int)    - The id of the message

    Return Value:
        Returns {} when successful 
    """
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']
    message_info = get_message_and_channel(message_id)

    if message_info is None:
        raise InputError(description = "message_id does not refer to a valid message within a channel/DM that the authorised user has joined")
    print(user_id)
    if message_info['type'] == 'channel':
        u_ids = [user['u_id'] for user in channels[message_info['channel_id']]['owner_members']]
        all_u_ids = [user['u_id'] for user in channels[message_info['channel_id']]['all_members']]
        print('\n\n\n\\n\n\n\n\n\n\n', user_id in u_ids)
        if user_id not in u_ids and user_id not in all_u_ids:
            raise InputError(description = "message_id is valid but user is not in channel")
        if message_info['message']['u_id'] != user_id and user_id not in u_ids:
            raise AccessError(description = "message_id is valid but user does not have permissions to edit")
    else:
        u_ids = [user['u_id'] for user in dms[message_info['dm_id']]['members']]
        if user_id not in u_ids or message_info['message']['u_id'] != user_id:
            raise AccessError(description = "message_id is valid but user does not have permissions to edit")
    message_info['channel']['messages'].remove(message_info['message'])
    store['channels'] = channels
    store['dms'] = dms
    data_store.set(store)
    return {}
    

def is_owner(user_id, channel):
    """ Check if a user is an owner of a channel """
    for owner in channel['owner_members']:
        if user_id == owner['u_id']:
            return True
    return False
    
def get_message_and_channel(message_id):
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']
    for key, channel in channels.items():
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'message': message, 'channel': channel, 'type': 'channel', 'channel_id': key}
    for key, channel in dms.items():
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'message': message, 'channel': channel, 'type': 'dm', 'dm_id': key}
    return None
