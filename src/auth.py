"""
Auth
Filename: auth.py

Author: Tetian Madfouni (z5361722), Samuel Bell (z5362604)
Created: 22.02.2022

Description: Allows the user to register an account and login to the account.
"""

import re
import hashlib
import jwt
from src.data_store import data_store
from src.error import AccessError, InputError

MAX_FIRST_NAME_LENGTH = 50
MAX_LAST_NAME_LENGTH = 50

GLOBAL_PERMISSION_OWNER = 2
GLOBAL_PERMISSION_USER = 1

JWT_SECRET = "COMP1531_H13A_CAMEL"


def auth_login_v1(email:str, password:str)->dict:
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
                jwt = create_JWT(user_id)
                return {'token': jwt, 'auth_user_id': user_id}
            else:
                raise InputError("Incorrect Password")
    raise InputError("Invalid Email")


def auth_register_v1(email: str, password: str, name_first: str, name_last:str)->dict:
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
    if not is_valid_email(email):
        raise InputError("Email is not valid")
    if len(password) < 6:
        raise InputError("Password is too short")
    if is_email_taken(email):
        raise InputError("Email is already taken")
    if len(name_first) < 1 or len(name_first) > MAX_FIRST_NAME_LENGTH:
        raise InputError("First name is too short or long")
    if len(name_last) < 1 or len(name_last) > MAX_LAST_NAME_LENGTH:
        raise InputError("Last name is too short or long")

    handle = generate_handle(name_first, name_last)

    store = data_store.get()
    users = store['users']
    new_user_id = len(users)
    global_permission = GLOBAL_PERMISSION_USER

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if new_user_id == 0:
        global_permission = GLOBAL_PERMISSION_OWNER
    new_user_dictionary = {'name_first': name_first, 'name_last': name_last, 'email': email,
    'password': hashed_password, 'handle': handle, 'global_permission': global_permission, 'sessions':[]}
    users[new_user_id] = new_user_dictionary
    data_store.set(store)
    jwt = create_JWT(new_user_id)
    return {'token': jwt, 'auth_user_id': new_user_id}

def auth_logout_v1(token):
    
    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")

    store = data_store.get()
    jwt_payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    
    user = store['users'][jwt_payload['auth_user_id']]
    user['sessions'].remove(jwt_payload['user_session_id'])

    return {}




def generate_handle(name_first:str, name_last:str)->str:
    """
    This function generates a handle for a user, the users first and last names
    are concatenated and turned lower case (if this is over 20 it is trimmed to 20).
    If that handle is taken a number is added to the end.

    Arguments:
        name_first (string)    - User's first name
        name_last (string)     - User's last name

    Return Value:
        Returns handle (string)

    """
    stripped_concatenated_name = remove_non_alphanumeric(name_first+name_last)
    stripped_concatenated_name = stripped_concatenated_name.lower()
    if len(stripped_concatenated_name) > 20:
        stripped_concatenated_name = stripped_concatenated_name[0:20]

    end_number = 0
    while is_handle_taken(stripped_concatenated_name):
        if end_number == 0:
            stripped_concatenated_name += str(end_number)
        else:
            stripped_concatenated_name = stripped_concatenated_name[:-1] + str(end_number)

        end_number += 1

    return stripped_concatenated_name


def is_email_taken(email:str)->bool:

    """
    Checks whether an email is used in the data store

    Arguments:
        email (string)    - The email to check

    Return Value:
        Returns True if it is taken
        Returns False if it is not taken

    """
    store = data_store.get()
    users = store['users']
    for user in users.values():
        if user['email'] == email:
            return True
    return False


def is_handle_taken(handle:str)->bool:
    """
    This function checks whether a handle is used before in the data store

    Arguments:
        handle (string)    - Handle to check

    Return Value:
        Returns True if the handle is taken
        Returns False if it is not taken

    """
    store = data_store.get()
    users = store['users']
    for user in users.values():
        if user['handle'] == handle:
            return True
    return False


def is_valid_email(email:str)->bool:
    """
    Verifies whether an email is valid or not

    Arguments:
        email (string)    - Email to check

    Return Value:
        Returns True if the email is valid and False if it is not
    """
    return bool(re.search(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email))


def remove_non_alphanumeric(string:str)->str:
    """
    Strips all alpha numeric characters from the input string

    Arguments:
        string (string)    - The string to have alphanumeric characters removed

    Return Value:
        Returns alnumString (string)
    """
    alnum_list = [char for char in string if char.isalnum()]
    return "".join(alnum_list)


def create_JWT(auth_user_id):
    store = data_store.get()
    new_session = len(store['users'][auth_user_id]['sessions'])
    store['users'][auth_user_id]['sessions'].append(new_session)
    payload = {'auth_user_id': auth_user_id, 'user_session_id': new_session}
    data_store.set(store)
    new_jwt = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return new_jwt

def is_valid_JWT(jwt_string):
    jwt_payload = jwt.decode(jwt_string, JWT_SECRET, algorithms=['HS256'])
    store = data_store.get()
    users = store['users']
    if jwt_payload['auth_user_id'] not in users:
        return False
    if jwt_payload['user_session_id'] not in users[jwt_payload['auth_user_id']]['sessions']:
        print("here2")
        return False
    return True