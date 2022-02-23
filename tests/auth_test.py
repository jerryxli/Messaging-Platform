import pytest

from src.auth import auth_login_v1, auth_register_v1, is_valid_email, remove_non_alphnum, is_handle_taken
from src.error import InputError, AccessError
from src.other import clear_v1

def test_valid_email():
    clear_v1()
    assert is_valid_email("jake@unsw.edu.au") == True
    assert is_valid_email("djjsksdj") == False
    assert is_valid_email("") == False
    assert is_valid_email("        ") == False

def test_remove_non_alphnum():
    clear_v1()
    assert remove_non_alphnum("") == ""
    assert remove_non_alphnum("^&^%^&^&") == ""
    assert remove_non_alphnum("1234567890") == "1234567890"
    assert remove_non_alphnum("abcdefghijklmnopqrstuvwxyz") == "abcdefghijklmnopqrstuvwxyz"
    assert remove_non_alphnum("this672^73 is a mixed ** passw8rd **") == "this67273isamixedpassw8rd"
    assert remove_non_alphnum("              ") == ""

def test_auth_register_v1():
    clear_v1()
    assert auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella") == {'auth_user_id': 0}
    assert auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs") == {'auth_user_id': 1}

def test_auth_register_v1_error_email_not_valid():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("tsgyd", "34rd^hds)", "Johnny", "Smith") # Email is not valid

def test_auth_register_v1_error_password_short():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("z55555@unsw.edu.au", "pa33", "Marc", "Chee")

def test_auth_register_v1_error_email_used():
    clear_v1()
    auth_register_v1("z123456789@unsw.edu.au", "thi3isn0t@pa33wor&", "Steve", "Jobs")
    with pytest.raises(InputError):
        auth_register_v1("z123456789@unsw.edu.au", "newpassword", "Steve", "Wozniak")

def test_auth_register_v1_error_first_name_bounds():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("z123456789@unsw.edu.au", "longpassword", "", "Li")
        auth_register_v1("245324@opedu.nsw.edu.au", "pass", "THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY", "Lastname")
        
def test_auth_register_v1_error_last_name_bounds():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("245324@opedu.nsw.edu.au", "pass", "Firstname", "THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY")
        auth_register_v1("z123456789@unsw.edu.au", "goodpass", "Simon", "")
