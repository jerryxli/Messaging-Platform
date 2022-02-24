from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
import pytest

#Basic Tests
def test_basic_success():
    clear_v1()
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
    assert auth_login_v1("z55555@unsw.edu.au","passwordlong") == {'auth_user_id': 0}

def test_incorrect_password():
    clear_v1()
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
    with pytest.raises(InputError):
        auth_login_v1("z55555@unsw.edu.au","passWRONG")

def test_invalid_email():
    clear_v1()
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs")   
    with pytest.raises(InputError):
        auth_login_v1("z1234@unsw.edu.au","passwordlong")

def test_complex_success():
    clear_v1()
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs") 
    auth_register_v1("z123@unsw.edu.au", "apples123", "Jacob", "Renzellid")
    auth_register_v1("z12345@unsw.edu.au","bananas&apricots","Apricot","IsNotAFirstName")
    assert auth_login_v1("z55555@unsw.edu.au","passwordlong") == {'auth_user_id': 0}
    assert auth_login_v1("z12345@unsw.edu.au","bananas&apricots") == {'auth_user_id': 3}
    with pytest.raises(InputError):
        auth_login_v1("z123@unsw.edu.au","wrongpasswordboi")


