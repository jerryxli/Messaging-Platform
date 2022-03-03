from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import verify_user

MAX_CHANNEL_NAME_LENGTH = 20

def channels_list_v1(auth_user_id:int)->dict:
    '''
    Prints out the list of channels that the user is a member of
    In the format: { channels: [{}, {}, {}] }

    Args:
    int auth_user_id
    '''
    # Gets list of channels from data_store
    store = data_store.get()
    channels = store['channels']

    # Creats a list to store channels with that user_id
    user_channels = []

    # Loops through each channel in the list Channels
    for channel_id, channel_details in channels.items():
        # Loops through each user for the channel
        if auth_user_id in channel_details['channel_members']:
            # If user_id match occurs, appends a dictionary with channel_id and name
            # into user_channels
            user_channel = {}
            user_channel['channel_id'] = channel_id
            user_channel['name'] = channel_details['name']
            user_channels.append(user_channel)
    # Returns a dictionary with the key 'channels' which has user_channels as its values
    return { 'channels': user_channels }

def channels_listall_v1(auth_user_id:int)->dict:
    '''
    Allows a registered user to list all public and private channels

    Arguments:
       int auth_user_id
    Exceptions:
        AccessError when auth_user_id is invalid
    Return Value:
        Returns list of channels and all their details in form: { channels }
    '''
    if verify_user(auth_user_id) is False:
        raise AccessError

    store = data_store.get()
    channels = store['channels']

    all_channels = []

    for key, channel in channels.items():
        user_channel = {}
        user_channel['channel_id'] = key
        user_channel['name'] = channel['name']

        all_channels.append(user_channel)

    return { 'channels': all_channels }

def channels_create_v1(auth_user_id:int, name:str, is_public:bool)->dict:
    '''
    Creates a new channel

    Arguments:
        auth_user_id (int)  - The id of the user
        name (string)       - Name of the channel
        is_public (bool)    - whether the channel is to be public or not

    Exceptions:
        InputError  - Occurs when channel name is too long or short
        AccessError - Occurs when user is not verified

    Return Value:
        Returns {channel_id} on successful creation

    Adds in format {'channel_id': int, 'name': str, 'public': bool, 'users': list(IDs)}
    '''
    store = data_store.get()
    channels = store['channels']
    if verify_user(auth_user_id) is False:
        raise AccessError("User not verified")
    if len(name) > MAX_CHANNEL_NAME_LENGTH or len(name) < 1:
        raise InputError("Channel name too long or short")
    if is_channel_taken(name) is True:
        raise InputError
    new_channel = {}
    new_channel_id = len(channels)
    new_channel['name'] = name
    new_channel['is_public'] = is_public
    new_channel['channel_owners'] = [auth_user_id]
    new_channel['channel_members'] = [auth_user_id]
    new_channel['messages'] = []
    channels[new_channel_id] = new_channel
    store['channels'] = channels
    data_store.set(store)
    return(
        {'channel_id': new_channel_id}
    )


def is_channel_taken(name:str)->bool:
    store = data_store.get()
    channels = store['channels']
    for channel in channels.values():
        if channel['name'] == name:
            return True
    return False
