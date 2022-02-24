from src.data_store import data_store
from src.error import InputError

#New push to test if pipeline will run
def auth_login_v1(email, password):
    store = data_store.get()
    users = store['users']
    for user in users:
        if email == user['email']:
            if password == user['password']:
                return {'auth_user_id': user['auth_user_id']}
            else:
                raise(InputError("Incorrect Password"))
    raise(InputError("Invalid Email"))

