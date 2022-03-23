from src.auth import JWT_SECRET
from src.data_store import data_store
import jwt

def clear_v1():
    """
    This function clears the data store environment for each test

    Arguments:
        None

    Return Value:
        None

    """
    store = data_store.get()
    store['users'] = {}
    store['channels'] = {}
    store['dms'] = {}
    store['messages'] = 0
    data_store.set(store)

def is_valid_dictionary_output(dictionary_output: dict, template_dictionary: dict) -> bool:
    """
    This function takes a dictionary output and determines whether it is structurally isomorphic
    to the template dictionary. This means that the keys must all be the same but the values can
    be anything as long as they are of the type specified in template dictionary.

    For example is_valid_dictionary({'auth_user_id': 2}, {'auth_user_id': int}) == True
                is_valid_dictionary({'auth_user_id': 787}, {'auth_user_id': int}) == True

                but

                is_valid_dictionary({'test': 'hello'}, {'auth_user_id': int}) == False

    Arguments:
        dictionary_output (dict)     - The dictionary which needs to be validated
        template_dictionary (dict)   - A dictionary with all the keys and types of values
                                       which the output will be checked against

    Exceptions:
        None

    Return Value:
        Returns a boolean value always
    """
    if not isinstance(dictionary_output,dict):
        return False
    if set(dictionary_output.keys()) != set(template_dictionary.keys()):
        return False
    for key in template_dictionary.keys():
        if not isinstance(dictionary_output[key], template_dictionary[key]):
            return False
    return True


def verify_user(auth_user_id: int)->bool:
    """
    This function takes a user ID and validates that they are registered in the system

    Arguments:
        auth_user_id (int)    - The id to validate

    Return Value:
        Returns True if it is registered, False if not

    """
    users = data_store.get()['users']
    return bool(auth_user_id in users.keys())

def is_global_user(auth_user_id: int)->bool:
    users = data_store.get()['users']
    return bool(users[auth_user_id]['global_permission'] == 2)

def user_id_from_JWT(token:str)->int:
    jwt_payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    return int(jwt_payload['auth_user_id'])