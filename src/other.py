from src.data_store import data_store
import jwt

JWT_SECRET = "COMP1531_H13A_CAMEL"

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