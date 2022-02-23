from src.data_store import data_store
from src.error import InputError
import re

MAX_FIRST_NAME_LENGTH = 50
MAX_LAST_NAME_LENGTH = 50

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    if not is_valid_email(email):
        raise InputError("Email is not valid")
    if len(password) < 6:
        raise InputError("Password is too short")
    if is_email_taken(email):
        raise InputError("Email is already taken")
    if len(name_first) == 0 or len(name_first) > MAX_FIRST_NAME_LENGTH:
        raise InputError("First name is too short or long")
    if len(name_last) == 0 or len(name_last) > MAX_LAST_NAME_LENGTH:
        raise InputError("Last name is too short or long")

    handle = generate_handle(name_first, name_last)

    store = data_store.get()
    users = store['users']

    new_user_id = len(users)

    new_user_dictionary = {'id': new_user_id, 'name_first': name_first, 'name_last': name_last, 'email': email, 'password': password, 'handle': handle}

    users.append(new_user_dictionary)

    data_store.set(store)

    return {
        'auth_user_id': new_user_id,
    }

def generate_handle(name_first, name_last):
    stripped_concatenated_name = remove_non_alphnum(name_first+name_last)
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

def is_email_taken(email):
    store = data_store.get()
    users = store['users']
    for user in users:
        if user['email'] == email:
            return True
    return False

def is_handle_taken(handle):
    store = data_store.get()
    users = store['users']
    for user in users:
        if user['handle'] == handle:
            return True
    return False


def is_valid_email(email):
    return bool(re.search('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email))

def remove_non_alphnum(string):
    alnumString = ''
    for character in string:
        if character.isalnum():
            alnumString += character
    return alnumString
