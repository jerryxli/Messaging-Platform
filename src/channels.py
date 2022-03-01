from ast import Store
from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import verify_user

MAX_CHANNEL_NAME_LENGTH = 20

def channels_list_v1(auth_user_id):
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

    # Checks each channel in list of channels for matching user_id
    for channel in channels: 
        # If user_id match occurs, appends a dictionary with channel_id and name
        # into user_channels

        for user in channel['channel_members']:
            if user == [auth_user_id]:
                user_channel = {}
                user_channel['channel_id'] = channel['channel_id']
                user_channel['name'] = channel['name']
                user_channels.append(user_channel)
    return { f"channels: {user_channels}" }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Adds in format {'channel_id': int, 'name': str, 'public': bool, 'users': list(IDs)}
    '''
    store = data_store.get()
    channels = store['channels']
    if verify_user(auth_user_id) == False:
        raise(AccessError)
    if len(name) > MAX_CHANNEL_NAME_LENGTH or len(name) < 1:
        raise(InputError)
    new_channel = {}
    new_channel['channel_id'] = len(channels)
    new_channel['name'] = name
    new_channel['is_public'] = is_public
    new_channel['users'] = [auth_user_id]
    channels.append(new_channel)
    store['channels'] = channels
    data_store.set(store)
    return(
        {'channel_id': new_channel['channel_id']}
    )

