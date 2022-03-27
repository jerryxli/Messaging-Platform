from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import GLOBAL_PERMISSION_REMOVED, MAX_FIRST_NAME_LENGTH, MAX_LAST_NAME_LENGTH, is_email_taken, is_valid_JWT, is_valid_email
from src.other import user_id_from_JWT, verify_user
from src.channel import GLOBAL_PERMISSION_OWNER, non_password_global_permission_field
from src.dm import dm_list_v1


def user_profile_v1(token: str, u_id: int)->dict:
    """
    Allows a user with token to get the profile of the specified u_id

    Arguments:
        token (str) - The token of the requesting user
        u_id  (int) - The id of the user to be looked up

    Errors:
        AccessError - Where the token passed is not valid
        InputError  - Where the u_id does not refer to a valid user

    Return Value:
        Dictionary containing u_id, email, name_first, name_last and handle_str
    """
    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if not verify_user(u_id):
        raise InputError(description="u_id does not refer to a valid user.")

    store = data_store.get()
    user = store['users'][u_id]

    return_dictionary = {'u_id': u_id, 'email': user['email'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle']}

    return return_dictionary


def user_setname_v1(token: str, name_first: str, name_last: str)->dict:
    """
    Allows a user with token to update their first and last name
    
    Arguments:
        token (str) - The token of the user who is updating details
        name_first  - The new first name
        name_last   - The new last name

    Errors:
        AccessError - Where the token is invalid
        InputError  - Where the first or last name is not between 1 and 50 characters
    
    Return Value:
        Empty Dictionary on Success
    
    """
    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if len(name_first) < 1 or len(name_first) > MAX_FIRST_NAME_LENGTH:
        raise InputError(description="The first name provided is not between 1 and 50 characters.")
    if len(name_last) < 1 or len(name_last) > MAX_LAST_NAME_LENGTH:
        raise InputError(description="The last name provided is not between 1 and 50 characters.")

    store = data_store.get()
    user = store['users'][user_id_from_JWT(token)]
    user['name_first'] = name_first
    user['name_last'] = name_last

    return {}


def user_setemail_v1(token: str, email: str)->dict:
    """
    Allows a user to update thier email

    Arguments:
        token (str) - The token of the user whose email has to be updated
        email (str) - The new email of the user

    Errors:
        AccessError when the token provided is not valid
        InputError when the email provided is not valid or is taken by another user

    Return Value:
        Empty dictionary on success
    
    """
    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if not is_valid_email(email):
        raise InputError(description="Email provided is not valid.")

    store = data_store.get()
    user = store['users'][user_id_from_JWT(token)]

    if user['email'] == email:
        return {}
    if is_email_taken(email):
        raise InputError(description="Email is already taken by another user.")

    user['email'] = email

    return {}


def users_all_v1(auth_user_id: int)->dict:
    """
    Gets all the users from the application

    Arguments:
        auth_user_id (int) - the user id of the caller
    
    Return Value:
        Dictionary containing 'users' which lists all users

    """
    store = data_store.get()
    users = store['users']
    all_users = []
    for user_id, user in users.items():
        if user['global_permission'] != GLOBAL_PERMISSION_REMOVED:
            user = non_password_global_permission_field(user)
            user['u_id'] = user_id
            user['handle_str'] = user.pop('handle')
            all_users.append(user)
    return {'users': all_users}


def user_remove_v1(token: str, u_id: int)->dict:
    store = data_store.get()
    users = store['users']
    admin_user = users[user_id_from_JWT(token)]
    if admin_user['global_permission'] != GLOBAL_PERMISSION_OWNER:
        raise AccessError(description="Insufficient permissions")
    if u_id not in users:
        raise InputError(description="Invalid user id")
    global_owners = {key: user for key, user in users.items() if user['global_permission'] == GLOBAL_PERMISSION_OWNER}
    if len(global_owners) == 1 and u_id in global_owners.keys():
        raise InputError(description="Would cause 0 owners of Seams")
    channels = store['channels']
    for channel in channels.values():
        admin_u_ids = [user['u_id'] for user in channel['owner_members']]
        member_u_ids = [user['u_id'] for user in channel['all_members']]
        if u_id in admin_u_ids:
            channel['owner_members'].pop(admin_u_ids.index(u_id))
        if u_id in member_u_ids:
            channel['all_members'].pop(member_u_ids.index(u_id))
        messages = channel['messages']
        for message in messages:
            if message['u_id'] == u_id:
                message['message'] = "Removed user"
        channel['messages'] = messages
    for dm in store['dms'].values():
        member_u_ids = [user['u_id'] for user in dm['members']]
        if u_id in member_u_ids:
            dm['members'].pop(member_u_ids.index(u_id))
        for message in dm['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    users[u_id] = {'name_first': 'Removed', 'name_last': 'user', 'email': '', 'password': '', 'handle': '', 'global_permission': GLOBAL_PERMISSION_REMOVED, 'sessions': []}
    store['channels'] = channels
    store['users'] = users
    data_store.set(store)
    return {}
