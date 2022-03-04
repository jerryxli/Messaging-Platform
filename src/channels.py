from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import verify_user

MAX_CHANNEL_NAME_LENGTH = 20

def channels_list_v1(auth_user_id:int)->dict:
    """
    Prints out the list of channels that the user is a member of
    In the format: { channels: [{}, {}, {}] }

    Args:
    int auth_user_id
    """
    if not verify_user(auth_user_id):
        raise AccessError("Auth id not valid")


    # Gets list of channels from data_store
    store = data_store.get()
    channels = store['channels']

    # Creats a list to store channels with that user_id
    user_channels = []
    # Loops through each channel in the list Channels
    for channel_id, channel_details in channels.items():
        # Loops through each user for the channel
        ids = [user['u_id'] for user in channel_details['all_members']]
        if auth_user_id in ids:
            # If user_id match occurs, appends a dictionary with channel_id and name
            # into user_channels
            user_channel = {'channel_id': channel_id, 'name': channel_details['name']}
            user_channels.append(user_channel)
    # Returns a dictionary with the key 'channels' which has user_channels as its values
    return { 'channels': user_channels }

def channels_listall_v1(auth_user_id:int)->dict:
    """
    Allows a registered user to list all public and private channels

    Arguments:
       int auth_user_id
    Exceptions:
        AccessError when auth_user_id is invalid
    Return Value:
        Returns list of channels and all their details in form: { channels }
    """
    if verify_user(auth_user_id) is False:
        raise AccessError

    store = data_store.get()
    channels = store['channels']
    return { 'channels': [{'channel_id': key, 'name': channel['name']} for key, channel in channels.items()] }

def channels_create_v1(auth_user_id:int, name:str, is_public:bool)->dict:
    """
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
    """
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    if verify_user(auth_user_id) == False:
        raise AccessError("User not verified")
    if len(name) > MAX_CHANNEL_NAME_LENGTH or len(name) < 1:
        raise InputError("Channel name too long or short")
    if is_channel_taken(name):
        raise InputError
    altered_users = {k: non_password_global_permission_field(v) for k,v in users.items()}
    for id, user in altered_users.items():
        user['u_id'] = id
        user['handle_str'] = user.pop('handle')
    new_channel_id = len(channels)
    channels[new_channel_id] = {'name': name, 'is_public': is_public, 'owner_members': [altered_users[auth_user_id]], 'all_members': [altered_users[auth_user_id]], 'messages': []}
    store['channels'] = channels
    data_store.set(store)
    return(
        {'channel_id': new_channel_id}
    )


def is_channel_taken(name:str)->bool:
    """
    Checks where channel name has already been used

    Arguments:
        name (str) - the desired name of the new channel
    
    Returns:
        Boolean, true if it already exists, false if it doesn't
    
    """
    store = data_store.get()
    channels = store['channels']
    names = [channel['name'] for channel in channels.values()]
    return bool(name in names)

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

