import json

from fastapi.testclient import TestClient
from unittest import TestCase
from unittest.mock import patch
from globals import app
import globals
from fastapi import status

# TODO: Implement auth endpoint tests, using TestClient, and attaching app for the test. Tests should be grouped inside ThreadsTests
# TODO: Import global variables, if needed
# https://fastapi.tiangolo.com/tutorial/testing/
# You can use local db for testing, without need to mock data
# If you need to mock data, use included patch
# Include all endpoints in tests. Only positive tests are needed for this assignment

client = TestClient(app)


class ThreadsTests(TestCase):
    def test_create_thread(self):
        response = client.post('/login', data=globals.user_2)

        access_token = json.loads(response.text)['access_token']

        response = client.post('/',
                               headers={"Authorization": f"Bearer {access_token}"},
                               json=globals.thread_1)

        assert response.status_code == status.HTTP_201_CREATED

        response = client.post('/',
                               headers={"Authorization": f"Bearer {access_token}"},
                               json=globals.thread_2)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_threads(self):
        response = client.get('/')
        assert response.status_code == status.HTTP_200_OK

    def test_get_thread(self):
        response = client.get(f'/{globals.thread_to_search_id}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_thread(self):
        response = client.post('/login', data=globals.user_2)

        access_token = json.loads(response.text)['access_token']

        response = client.put(f'/{globals.thread_to_update_id}',
                              headers={"Authorization": f"Bearer {access_token}"},
                              json=globals.thread_to_update)

        assert response.status_code == status.HTTP_200_OK

    def test_delete_thread(self):
        response = client.post('/login', data=globals.user_2)

        access_token = json.loads(response.text)['access_token']

        response = client.delete(f'/{globals.thread_to_delete_id}',
                                 headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == status.HTTP_200_OK
