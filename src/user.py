from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import MAX_FIRST_NAME_LENGTH, MAX_LAST_NAME_LENGTH, is_email_taken, is_valid_JWT, is_valid_email
from src.other import user_id_from_JWT, verify_user
from src.channel import non_password_global_permission_field

def user_profile_v1(token:str, u_id:int)->dict:

    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if not verify_user(u_id):
        raise InputError(description="u_id does not refer to a valid user.")
    
    store = data_store.get()
    user = store['users'][u_id]

    return_dictionary = {'u_id':u_id, 'email': user['email'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle']}

    return return_dictionary

def user_setname_v1(token:str, name_first:str, name_last: str)->dict:
    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if len(name_first) < 1 or len(name_first) > MAX_FIRST_NAME_LENGTH:
        raise InputError(description="The first name provided is not between 1 and 50 characters(inclusive).")
    if len(name_last) < 1 or len(name_last) > MAX_LAST_NAME_LENGTH:
        raise InputError(description="The last name provided is not between 1 and 50 characters(inclusive).")

    store = data_store.get()
    user = store['users'][user_id_from_JWT(token)]
    user['name_first'] = name_first
    user['name_last'] = name_last

    return {}

def user_setemail_v1(token:str, email:str)->dict:
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

def users_all_v1(auth_user_id:int)->dict:
    store = data_store.get()
    users = store['users']
    all_users = []
    for user_id, user in users.items():
        user = non_password_global_permission_field(user)
        user['u_id'] = user_id
        user['handle_str'] = user.pop('handle')
        all_users.append(user)
    return { 'users': all_users }