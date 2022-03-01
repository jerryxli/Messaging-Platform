from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import verify_user

MAX_CHANNEL_NAME_LENGTH = 20

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

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
    if verify_user(auth_user_id) == False:
        raise AccessError("User not verified")
    if len(name) > MAX_CHANNEL_NAME_LENGTH or len(name) < 1:
        raise InputError("Channel name too long or short")
    new_channel = {}
    new_channel['channel_id'] = len(channels)
    new_channel['name'] = name
    new_channel['is_public'] = is_public
    new_channel['users'] = [auth_user_id]
    channels.append(new_channel)
    store['channels'] = channels
    data_store.set(store)
    return {'channel_id': new_channel['channel_id']}
