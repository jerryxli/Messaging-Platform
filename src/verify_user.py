from src.data_store import data_store
from src.error import AccessError, InputError
 

def verify_user(auth_user_id):
    users = data_store.get()['users']
    for user in users:
        if auth_user_id == user['auth_user_id']:
            verified = 1
    if verified == 0:
        return False
    else:
        return True