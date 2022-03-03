from src.data_store import data_store

def clear_v1():
    store = data_store.get()
    store['users'] = {}
    store['channels'] = {}
    data_store.set(store)

'''
This function takes a dictionary output and determines whether it is structurally isomorphic
to the template dictionary. This means that the keys must all be the same but the values can
be anything as long as they are of the type specified in template dictionary.

For example is_valid_dictionary({'auth_user_id': 2}, {'auth_user_id': int}) == True
            is_valid_dictionary({'auth_user_id': 787}, {'auth_user_id': int}) == True

            but

            is_valid_dictionary({'test': 'hello'}, {'auth_user_id': int}) == False

Arguments:
    dictionary_output (dict)     - The dictionary which needs to be validated
    template_dictionary (dict)   - A dictionary with all the keys and types of values which the output will be checked against

Exceptions:
    None

Return Value:
    Returns a boolean value always
'''
def is_valid_dictionary_output(dictionary_output: dict, template_dictionary: dict) -> bool:
    if type(dictionary_output) != dict:
        return False
    if set(dictionary_output.keys()) != set(template_dictionary.keys()):
        return False
    for key in template_dictionary.keys():
        if type(dictionary_output[key]) != template_dictionary[key]:
            return False
    return True
    

'''
This function takes a user ID and validates that they are registered in the system
'''
def verify_user(auth_user_id):
    users = data_store.get()['users']
    if auth_user_id in users.keys():
        return True
    else:
        return False
    