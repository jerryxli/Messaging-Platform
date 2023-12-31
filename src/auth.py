"""
Auth
Filename: auth.py

Author: Tetian Madfouni (z5361722), Samuel Bell (z5362604)
Created: 22.02.2022

Description: Allows the user to register an account and login to the account.
"""

import hashlib
import jwt
from src.data_store import data_store
from src.error import AccessError, InputError
import src.other as other
from time import time
from src.config import port

def auth_login_v2(email: str, password: str)->dict:
    """
    Logs an existing user into the application

    Arguments:
        email (string)      - User's email
        password (string)   - User's password

    Exceptions:
        InputError  - Occurs when email is invalid or incorrect password entered

    Return Value:
        Returns {auth_user_id} on successful login

    """
    store = data_store.get()
    users = store['users']

    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    for user_id, user in users.items():
        if email == user['email']:
            if hashed_input == user['password']:
                jwt = other.create_JWT(user_id)
                return {'token': jwt, 'auth_user_id': user_id}
            else:
                raise InputError(description="Incorrect Password")
    raise InputError(description="Invalid Email")


def auth_register_v2(email: str, password: str, name_first: str, name_last: str)->dict:
    """
    Registers a user into the database, generates a handle upon registration

    Arguments:
        email (string)      - The email of the prospective user
        password (string)   - the password of the user
        name_first (string) - User's first name
        name_last (string)  - User's last name

    Exceptions:
        InputError  - Occurs when email is not valid,
                                password is less than 6 characters,
                                first name or last name is not between 1 and 50 characters

    Return Value:
        Returns {auth_user_id} on successful registration

    """
    if not other.is_valid_email(email):
        raise InputError(description="Email is not valid")
    if len(password) < 6:
        raise InputError(description="Password is too short")
    if other.is_email_taken(email):
        raise InputError(description="Email is already taken")
    if len(name_first) < 1 or len(name_first) > other.MAX_FIRST_NAME_LENGTH:
        raise InputError(description="First name is too short or long")
    if len(name_last) < 1 or len(name_last) > other.MAX_LAST_NAME_LENGTH:
        raise InputError(description="Last name is too short or long")

    handle = other.generate_handle(name_first, name_last)

    store = data_store.get()
    users = store['users']
    user_stats = store['user_stats']
    new_user_id = len(users)
    global_permission = other.GLOBAL_PERMISSION_USER

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if new_user_id == 0:
        global_permission = other.GLOBAL_PERMISSION_OWNER
        store['server_stats'] = {'time_created': time(), 'stats': [{'num_channels':0, 'num_dms':0, 'num_msg': 0, 'time': time()}]}
    new_user_dictionary = {'name_first': name_first, 'name_last': name_last, 'email': email,
                           'password': hashed_password, 'handle': handle, 'global_permission': global_permission, 
                           'sessions': [], 'profile_img_url': f"http://localhost:{port}/static/default.jpg"}
    users[new_user_id] = new_user_dictionary
    new_user_stats = {'time_created': time(), 'stats': [{'num_channels':0, 'num_dms':0, 'num_msg': 0, 'time': time()}]}
    user_stats[new_user_id] = new_user_stats
    data_store.set(store)
    jwt = other.create_JWT(new_user_id)
    return {'token': jwt, 'auth_user_id': new_user_id}


def auth_logout_v1(token):
    """
    Logs the user out of the session in the token

    Arguments:
        token (str) - The token from the session which the user wants to be logged out of

    Errors:
        AccessError if the token is not valid or does not refer to a valid session

    Return value:
        {}
    
    """

    if not other.is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")

    store = data_store.get()
    jwt_payload = jwt.decode(token, other.JWT_SECRET, algorithms=['HS256'])
    
    user = store['users'][jwt_payload['auth_user_id']]
    user['sessions'].remove(jwt_payload['user_session_id'])

    return {}


def change_global_permission(auth_user_id:str, u_id:int, new_perm:int)->dict:
    """
    Allows for global permissions to be changed

    Arguments:
        auth_user_id (int) - User exacting the change
        u_id (int)         - User to have permissions changed
        new_perm (int)     - New permission

    Errors:
        AccessError when the user changing permissions is not authorised
        InputError where permission would leave no global owner, where permission doesn't exist or 
                         where permission is the same

    Return Values:

    """
    store = data_store.get()
    users = store['users']
    global_owners = [key for key, user in users.items() if user['global_permission'] == other.GLOBAL_PERMISSION_OWNER]
    if auth_user_id not in global_owners:
        raise AccessError(description="User is not an owner")
    if len(global_owners) == 1 and u_id in global_owners and new_perm == other.GLOBAL_PERMISSION_USER:
        raise InputError(description="This action would leave server without any owners")
    if new_perm not in [other.GLOBAL_PERMISSION_USER, other.GLOBAL_PERMISSION_OWNER]:
        raise InputError(description="This permission doesn't exist")
    
    if u_id in users.keys():
        user = users[u_id]
        if user['global_permission'] == new_perm:
            raise InputError(description="This user already has this permission")
        user['global_permission'] = new_perm
        data_store.set(store)
    else:
        raise InputError(description="There is no user with this id")
