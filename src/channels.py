from src.error import InputError, AccessError
from src.data_store import data_store
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

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Adds in format {'channel_id': int, 'name': str, 'public': bool, 'users': list(IDs)}
    '''
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    verified = 0
    for user in users:
        if auth_user_id == user['auth_user_id']:
            verified = 1
    print(verified)
    if verified == 0:
        raise(AccessError)
    if len(name) > MAX_CHANNEL_NAME_LENGTH or len(name) < 1:
        raise(InputError)
    new_channel = {}
    new_channel['channel_id'] = len(channels) + 1
    new_channel['name'] = name
    new_channel['is_public'] = is_public
    new_channel['users'] = [auth_user_id]
    channels.append(new_channel)
    store['channels'] = channels
    data_store.set(store)


    
