"""
Message
Filename: message.py

Author: Tetian Madfouni (z5361722), Jacqueline Chen (z5360310), Leo Shi (z5364321),
Samuel Bell (z5362604), Jerry Li (z5362290)
Created: 19.03.2022

Description: Allows the user to send, edit and remove messages.
"""

from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import verify_user, is_global_user

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
    messages = store['messages']
    message_channel = get_channel(channel_id)

    if len(message) > 1000 or len(message) < 1:
        raise InputError("Length of message is less than 1 or over 1000 characters")
    
    new_message_id += len(messages)

    if message_channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    for user in message_channel['users']:
        if user['user_id'] == user_id:
            messages[new_message_id] = {'message_id': new_message_id, 'user_id': user, 'message': message}
            data_store.set(store)
            return ({'message_id': new_message_id})
    raise AccessError("channel_id is valid and the user is not a member of the channel")
    
def message_edit_v1():
    pass

def message_remove_v1():
    pass

def get_user_from_token(token):
    # something to do with the jwt of token
    pass

def get_channel(channel_id):
    store = data_store.get()
    channels = store['channels']
    for channel in channels:
        if channel_id == channel['channel_id']:
            return channel
    return None
