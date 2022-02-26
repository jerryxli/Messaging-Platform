# Test file for other.py
import pytest
from src.other import clear_v1, is_valid_dictionary_output


def test_clear_v1():
    pass

def test_is_valid_dictionary_output():
    assert is_valid_dictionary_output({},{})
    assert is_valid_dictionary_output({'channel_id': 0}, {'channel_id': int})
    assert is_valid_dictionary_output({'channel_id': 3242}, {'channel_id': int})
    assert not is_valid_dictionary_output({}, {'channel_id': int})
    assert not is_valid_dictionary_output({'auth_id': 9}, {'channel_id': int})
    assert not is_valid_dictionary_output({'auth_id':9, 'channel_id': 2}, {'channel_id': int})
    assert not is_valid_dictionary_output({'auth_id': 'hello'}, {'auth_id': int})
    assert not is_valid_dictionary_output('hello', {})