import requests
import jwt
import pytest
from src.auth import JWT_SECRET
from src.config import url

REGISTER_URL = f"{url}/auth/register/v2"
PROFILE_URL = f"{url}/user/profile/v1"

@pytest.fixture
def clear_store():
    requests.delete(f"{url}/clear/v1", json={})


def test_forged_token(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    auth_id = int(response.json()['auth_user_id'])
    forged_encoding = {"auth_user_id": auth_id + 1, "session_id": 1000}
    forgedJWT = jwt.encode(forged_encoding, "faketoken", algorithm='HS256')
    profile_repsonse_0 = requests.get(PROFILE_URL, params={"u_id": auth_id, "token": forgedJWT})
    assert profile_repsonse_0.status_code == 403

def test_token_exceeding_users(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    auth_id = int(response.json()['auth_user_id'])
    forged_encoding = {"auth_user_id": auth_id + 1, "session_id": 1000}
    forgedJWT = jwt.encode(forged_encoding, JWT_SECRET, algorithm='HS256')
    profile_repsonse_0 = requests.get(PROFILE_URL, params={"u_id": auth_id, "token": forgedJWT})
    assert profile_repsonse_0.status_code == 403

def test_manually_forged_with_correct_u_id(clear_store):
    response = requests.post(REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    profile_res = requests.get(PROFILE_URL, params={'u_id': response.json()['auth_user_id'], "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX3VzZXJfaWQiOjEzLCJ1c2VyX3Nlc3Npb25faWQiOjB9.VQ0yytHPCXtCAlDdvb1QVzpi95TMmI6hmlFWTe2tq88"})
    assert profile_res.status_code == 403