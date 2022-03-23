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
    
def message_edit_v1():
    pass

def message_remove_v1():
    pass
