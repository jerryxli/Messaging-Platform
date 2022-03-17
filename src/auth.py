from logging import NullHandler
import re
from src.data_store import data_store
from src.error import InputError

MAX_FIRST_NAME_LENGTH = 50
MAX_LAST_NAME_LENGTH = 50

GLOBAL_PERMISSION_OWNER = 2
GLOBAL_PERMISSION_USER = 1

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
    for user_id, user in users.items():
        if email == user['email']:
            if password == user['password']:
                return {'auth_user_id': user_id}
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
        name_last (string)  - User's last naem

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
    if new_user_id == 0:
        global_permission = GLOBAL_PERMISSION_OWNER
    new_user_dictionary = {'name_first': name_first, 'name_last': name_last, 'email': email, 'password': password, 'handle': handle, 'global_permission': global_permission}
    users[new_user_id] = new_user_dictionary
    data_store.set(store)
    return {'auth_user_id': new_user_id}


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


def change_global_permission(u_id:int, new_perm:int)->dict:
    '''
    Needs JWT check once implemented by login
    '''
    store = data_store.get()
    users = store['users']
    print(users)
    global_owners = {key: user for key, user in users.items() if user['global_permission'] == GLOBAL_PERMISSION_OWNER}
    if len(global_owners) == 1 and u_id in global_owners.keys() and new_perm == GLOBAL_PERMISSION_USER:
        raise InputError
    if new_perm not in [GLOBAL_PERMISSION_USER, GLOBAL_PERMISSION_OWNER]:
        raise InputError
    
    if u_id in users.keys():
        user = users[u_id]
        if user['global_permission'] == new_perm:
            raise InputError
        user['global_permission'] = new_perm
        data_store.set(store)
    else:
        raise InputError
