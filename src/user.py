from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import is_valid_JWT
from src.other import verify_user

def user_profile_v1(token:str, u_id:int)->dict:

    if not is_valid_JWT(token):
        raise AccessError(description="The token provided is not valid.")
    if not verify_user(u_id):
        raise InputError(description="u_id does not refer to a valid user.")
    
    store = data_store.get()
    user = store['users'][u_id]

    return_dictionary = {'u_id':u_id, 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle']}

    return return_dictionary