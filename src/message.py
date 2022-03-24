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
from src.other import verify_user, is_global_user
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
        raise InputError("channel_id does not refer to a valid channel")
        
    if len(message) > 1000 or len(message) < 1:
        raise InputError("Length of message is less than 1 or over 1000 characters")

    if check_user_in_channel(user_id, message_channel):
        new_message_id = store['messages']
        message_channel['messages'].append({'message_id': new_message_id, 'u_id': user_id, 'message': message, 'time_sent': time()})
        store['channels'] = channels
        store['messages'] += 1
        data_store.set(store)
        return ({'message_id': new_message_id})
    else:
        raise AccessError("channel_id is valid and the user is not a member of the channel")

    
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
        raise InputError("message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

    # check if user is in the channel
    if not check_user_in_channel(message_info['message']['u_id'], message_info['channel']):
        raise InputError("message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

    if message_info['message']['u_id'] != user_id:
        raise AccessError("message_id is valid and the message was not sent by the user trying to edit")

    if len(message) > 1000:
        raise InputError("message over 1000 characters")
    
    if is_owner(user_id, message_info['channel']):
        if message == '':
            message_remove_v1(user_id, message_id)
        # edit the message
        message_info['message']['message'] = message
        store['channels'] = channels
        store['dms'] = dms
        data_store.set(store)
        return {}
    else:
        raise AccessError("message_id is valid and the user does not have owner permissions in the channel/DM")



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

    #  message_id is invalid
    if message_info is None:
        raise InputError("message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

    # check if user is in the channel
    if not check_user_in_channel(message_info['message']['u_id'], message_info['channel']):
        raise InputError("message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

    if message_info['message']['u_id'] != user_id:
        raise AccessError("message_id is valid and the message was not sent by the user trying to edit")

    # check for owner
    if is_owner(user_id, message_info['channel']):
        message_info['channel']['messages'].remove(message_info['message'])
        store['channels'] = channels
        store['dms'] = dms
        data_store.set(store)
        return {}
    else:
        raise AccessError("message_id is valid and the user does not have owner permissions in the channel/DM")
    

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
    for channel in channels.values():
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'message': message, 'channel': channel}
    for channel in dms.values():
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'message': message, 'channel': channel}
    return None
