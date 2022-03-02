from src.data_store import data_store
from src.error import AccessError, InputError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

# given a channel id, return a channel dictionary
def get_channel(id):
    store = data_store.get()
    channels = store['channels']
    for channel in channels:
        if int(id) == channel['channel_id']:
            return channel
    return None

# check if the user is already in the channel
def check_user_in_channel(user_id, channel):
    for member in channel['channel_members']:
        if user_id == member:
            return True
    return False

# Append the user info into the respective lists
def get_user_details(auth_user_id):
    # Accesses the data_store to get the objects
    store = data_store.get()
    users = store['users']
    
    # Loops through users to append info
    for user in users:
        if auth_user_id == user['auth_user_id']:
            details = {}
            details['u_id'] = user['auth_user_id']
            details['email'] = user['email']
            details['name_first'] = user['name_first']
            details['name_last'] = user['name_last']
            details['handle_str'] = user['handle']
    return details


def channel_details_v1(auth_user_id, channel_id):
    '''
    Returns the details of a channel in the format:
    { name: , is_public: , owner_members: [], all_members: [], }
    '''
    # Checks for Input error: when the channel_id does not exist
    if get_channel(channel_id) == None:
        raise(InputError)
    channel = get_channel(channel_id)
    # Checks for Access error: when the user is not a member of the channel
    if check_user_in_channel(auth_user_id, channel) == False:
        raise(AccessError)
    
    # Create a blank dictionary that will contain the channel details
    channel_details = {}

    # Add the details into the channel_details dictionary
    channel_details['name'] = channel['name']
    channel_details['is_public'] = channel['is_public']
    channel_details['owner_members'] = []
    channel_details['all_members'] = []

    # Append the user info into the owner_members list
    owner_members = channel_details['owner_members']
    for owner in channel['channel_owners']:
        owner_members.append(get_user_details(owner))

    # Append the members info into all_members list
    all_members = channel_details['all_members']
    for member in channel['channel_members']: 
        all_members.append(get_user_details(member))

    return channel_details

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    channel = get_channel(channel_id)  
    if check_user_in_channel(auth_user_id, channel) == False:
        channel['channel_members'].append(auth_user_id)

    return {}
