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
import src.other as other


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
        raise InputError(
            description="channel_id does not refer to a valid channel")

    if len(message) > 1000 or len(message) < 1:
        raise InputError(
            description="Length of message is less than 1 or over 1000 characters")
    if not other.check_user_in_channel(user_id, message_channel):
        raise AccessError(
            description="channel_id is valid and the user is not a member of the channel")
    messages = store['messages']
    new_message_id = len(messages)
    messages[new_message_id] = {'message_id': new_message_id, 'u_id': user_id,
                                'message': message, 'time_sent': time(), 'is_channel': True, 'id': channel_id, 'react_id': 1, 'react_u_ids': []}
    data_store.set(store)
    return ({'message_id': new_message_id})


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
    messages = store['messages']
    channels = store['channels']
    dms = store['dms']
    if message_id not in messages:
        raise InputError(
            description="message_id does not refer to a valid message")
    else:
        curr_message = messages[message_id]
    if curr_message['is_channel'] == True:
        u_ids = [user['u_id']
                 for user in channels[curr_message['id']]['owner_members']]
        all_u_ids = [user['u_id']
                     for user in channels[curr_message['id']]['all_members']]
        if user_id not in u_ids and user_id not in all_u_ids:
            raise InputError(
                description="message_id is valid but user is not in channel")
        if curr_message['u_id'] != user_id and user_id not in u_ids:
            raise AccessError(
                description="message_id is valid but user does not have permissions to edit")
    else:
        u_ids = [user['u_id'] for user in dms[curr_message['id']]['members']]
        if user_id not in u_ids:
            raise InputError(
                description="message_id is valid but user is not in dm")
    if len(message) > 1000:
        raise InputError(description="message over 1000 characters")
    if message == '':
        message_remove_v1(user_id, message_id)
    else:
        curr_message['message'] = message
        messages['message'] = curr_message
        store['messages'] = messages
        print(store)
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
    messages = store['messages']
    if message_id not in messages:
        raise InputError(
            description="message_id does not refer to a valid message")
    else:
        message = messages[message_id]
    if message['is_channel'] == True:
        u_ids = [user['u_id']
                 for user in channels[message['id']]['owner_members']]
        all_u_ids = [user['u_id']
                     for user in channels[message['id']]['all_members']]
        if user_id not in u_ids and user_id not in all_u_ids:
            raise InputError(
                description="message_id is valid but user is not in channel")
        if message['u_id'] != user_id and user_id not in u_ids:
            raise AccessError(
                description="message_id is valid but user does not have permissions to remove")
    else:
        u_ids = [user['u_id'] for user in dms[message['id']]['members']]
        if user_id not in u_ids:
            raise InputError(
                description="message_id is valid but user is not in dm")
    messages.pop(message['id'])
    store['messages'] = messages
    data_store.set(store)
    return {}


def message_react_v1(user_id, message_id, react_id):
    """
    Given a message_id for a message, the authroised user adds a 'react' to the message from the channel/DM

    Exceptions:
        InputError      - Occurs when the message_id is not a valid message within the channel
        InputError      - Occurs when the react_id is not a valid react ID, ie != 1
        InputError      - Occurs when the message already contains a react with ID react_id

    Arguments:
        token (int)         - The token of the user
        message_id (int)    - The id of the message
        react_id (int)      - The id of the react (1 == valid, 0 == invalid)

    Return Value:
        Returns {} when successful 
    """

    store = data_store.get()
    channels = store['channels']
    dms = store['dms']
    messages = store['messages']

    if message_id not in messages:
        raise InputError(
            description="message_id does not refer to a valid message")
    else:
        message = messages[message_id]
    if message['is_channel'] == True:
        u_ids = [user['u_id']
                 for user in channels[message['id']]['owner_members']]
        all_u_ids = [user['u_id']
                     for user in channels[message['id']]['all_members']]
        if user_id not in u_ids and user_id not in all_u_ids:
            raise InputError(
                description="message_id is not a valid message within the channel")
    else:
        u_ids = [user['u_id'] for user in dms[message['id']]['members']]
        if user_id not in u_ids:
            raise InputError(
                description="message_id is not a valid message within the dm")

    # add react
    if message['react_id'] == react_id:
        if user_id not in message['react_u_ids']:
            message['react_u_ids'].append(user_id)
        else:
            raise InputError(
                description="message already contains a react from this user")
    else:
        raise InputError(description="react_id is not valid")
    store['messages'] = messages
    data_store.set(store)
    return {}
