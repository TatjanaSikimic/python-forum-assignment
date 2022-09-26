import json

from fastapi.testclient import TestClient
from fastapi import status, FastAPI
from unittest import TestCase
from unittest.mock import patch

# TODO: Implement auth endpoint tests, using TestClient, and attaching app for the test. Tests should be grouped inside AuthTests
# TODO: Import global variables, if needed
# https://fastapi.tiangolo.com/tutorial/testing/
import globals
from globals import app

client = TestClient(app)

class AuthTests(TestCase):
    # def test_register_user(self):
    #     response = client.post('/register',
    #                            json=globals.user_2)
    #
    #     assert response.status_code == status.HTTP_201_CREATED

    def test_login_user(self):
        response = client.post('/login', data=globals.user_2)

        access_token = json.loads(response.text)['access_token']
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'access_token': f'{access_token}'}

    def test_log_out(self):
        response = client.post('/login', data=globals.user_2)

        access_token = json.loads(response.text)['access_token']

        response = client.post('/logout', headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == status.HTTP_200_OK




