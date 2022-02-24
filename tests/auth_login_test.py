<<<<<<< HEAD
<<<<<<<< HEAD:tests/auth_login_test.py
from src.auth import auth_register_v1, auth_login_v1
=======
from src.auth import auth_login_v1
from src.auth import auth_register_v1
>>>>>>> master
from src.error import InputError, AccessError
from src.other import clear_v1

import pytest

#Basic Tests
def test_basic_success():
    clear_v1()
<<<<<<< HEAD
=======

>>>>>>> master
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
    assert auth_login_v1("z55555@unsw.edu.au","passwordlong") == {'auth_user_id': 0}

def test_incorrect_password():
    clear_v1()
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
<<<<<<< HEAD
=======

>>>>>>> master
    with pytest.raises(InputError):
        auth_login_v1("z55555@unsw.edu.au","passWRONG")

def test_invalid_email():
    clear_v1()
<<<<<<< HEAD
=======

>>>>>>> master
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs")   
    with pytest.raises(InputError):
        auth_login_v1("z1234@unsw.edu.au","passwordlong")

def test_complex_success():
    clear_v1()
    auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella")
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs") 
<<<<<<< HEAD
=======

>>>>>>> master
    auth_register_v1("z123@unsw.edu.au", "apples123", "Jacob", "Renzellid")
    auth_register_v1("z12345@unsw.edu.au","bananas&apricots","Apricot","IsNotAFirstName")
    assert auth_login_v1("z55555@unsw.edu.au","passwordlong") == {'auth_user_id': 0}
    assert auth_login_v1("z12345@unsw.edu.au","bananas&apricots") == {'auth_user_id': 3}
    with pytest.raises(InputError):
        auth_login_v1("z123@unsw.edu.au","wrongpasswordboi")

<<<<<<< HEAD

========
import pytest

from src.auth import auth_login_v1, auth_register_v1, generate_handle, is_email_taken, is_valid_email, remove_non_alphnum, is_handle_taken
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def clear_store():
    clear_v1()


def test_valid_email(clear_store):
    assert is_valid_email("jake@unsw.edu.au") == True
    assert is_valid_email("djjsksdj") == False
    assert is_valid_email("") == False
    assert is_valid_email("        ") == False

def test_remove_non_alphnum(clear_store):
    assert remove_non_alphnum("") == ""
    assert remove_non_alphnum("^&^%^&^&") == ""
    assert remove_non_alphnum("1234567890") == "1234567890"
    assert remove_non_alphnum("abcdefghijklmnopqrstuvwxyz") == "abcdefghijklmnopqrstuvwxyz"
    assert remove_non_alphnum("this672^73 is a mixed ** passw8rd **") == "this67273isamixedpassw8rd"
    assert remove_non_alphnum("              ") == ""

def test_is_email_taken(clear_store):
    assert is_email_taken("hello@test.unsw.edu.au") == False
    auth_register_v1("hello@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    assert is_email_taken("hello@unsw.edu.au") == True
    assert is_email_taken("ello@test.com.au") == False

def test_is_handle_taken(clear_store):
    assert is_handle_taken("haydensmith") == False
    auth_register_v1("z555@unsw.edu.au", "passwordlong", "Hayden", "Smith")
    assert is_handle_taken("haydensmith") == True
    assert is_handle_taken("haydensmith1") == False

def test_generate_handle(clear_store):
    assert generate_handle("Hayden", "Jacobs") == "haydenjacobs"
    auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs")
    assert generate_handle("Hayden", "Jacobs") == "haydenjacobs0"
    auth_register_v1("z09373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs")
    assert generate_handle("Hayden", "Jacobs") == "haydenjacobs1"
    auth_register_v1("z328373@unsw.edu.au", "passwordlong", "abcdefghijklmnopqrstuvwxyz", "Jacobs")
    assert generate_handle("abcdefghijklmnopqrstuvwxyz", "ls") == "abcdefghijklmnopqrst0"


def test_auth_register_v1(clear_store):
    assert auth_register_v1("z55555@unsw.edu.au", "passwordlong", "Jake", "Renzella") == {'auth_user_id': 0}
    assert auth_register_v1("z09328373@unsw.edu.au", "passwordlong", "Hayden", "Jacobs") == {'auth_user_id': 1}


def test_auth_register_v1_error_email_not_valid(clear_store):
    with pytest.raises(InputError):
        auth_register_v1("tsgyd", "34rd^hds)", "Johnny", "Smith") # Email is not valid

def test_auth_register_v1_error_password_short(clear_store):
    with pytest.raises(InputError):
        auth_register_v1("z55555@unsw.edu.au", "pa33", "Marc", "Chee")


def test_auth_register_v1_error_email_used(clear_store):
    auth_register_v1("z123456789@unsw.edu.au", "thi3isn0t@pa33wor&", "Steve", "Jobs")
    with pytest.raises(InputError):
        auth_register_v1("z123456789@unsw.edu.au", "newpassword", "Steve", "Wozniak")


def test_auth_register_v1_error_first_name_short(clear_store):
    with pytest.raises(InputError):
        auth_register_v1("z123456789@unsw.edu.au", "longpassword", "", "Li")


def test_auth_register_v1_error_first_name_long(clear_store):
    with pytest.raises(InputError):
        auth_register_v1("245324@opedu.nsw.edu.au", "pass", "THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY", "Lastname")
        

def test_auth_register_v1_error_last_name_short(clear_store):
    with pytest.raises(InputError):
        auth_register_v1("z123456789@unsw.edu.au", "goodpass", "Simon", "")


def test_auth_register_v1_error_last_name_long(clear_store):
    with pytest.raises(InputError):
<<<<<<< HEAD

=======
        auth_register_v1("245324@opedu.nsw.edu.au", "pass", "Firstname", "THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY")
>>>>>>> 61140bdd3ffb8c05c0b1c7e1527dd179d2425e79
>>>>>>>> master:tests/auth_test.py
=======
>>>>>>> master
