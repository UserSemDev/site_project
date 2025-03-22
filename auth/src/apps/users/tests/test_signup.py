import json

import pytest
from apps.users.models import User
from apps.users.utils import generate_jwt
from django.test import Client
from mongoengine import connect, disconnect
from testcontainers.mongodb import MongoDbContainer


class TestAuth:
    client = Client()

    @pytest.fixture(scope="session")
    def mongo_container(self):
        with MongoDbContainer("mongo:latest") as mongo:
            yield mongo

    @pytest.fixture(scope="function", autouse=True)
    def clear_db(self, mongo_container):
        disconnect()

        connection_url = mongo_container.get_connection_url()
        connect(host=connection_url)

        from mongoengine.connection import get_db

        db = get_db()
        db.user.delete_many({})
        yield db
        db.user.delete_many({})
        disconnect()

    @pytest.fixture
    def first_user(self):
        user = User(username="test_user", email="test_user@example.com")
        user.set_password("test_password")
        user.save()
        return user

    @pytest.fixture
    def auth_token(self, first_user):
        return generate_jwt(first_user.id)

    @pytest.mark.unit
    def test_signup_success(self):
        data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "test_password",
        }

        response = self.client.post(
            "/signup/", data=data, content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json()["jwt"]

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "payload, excepted_status",
        [
            ("{}", 400),
            ("{broken_json", 400),
            ('{"username": "test_username"}', 400),
            ('{"email": "test_username@example.com"}', 400),
            ('{"password": "test_password"}', 400),
            ('{"role": "user"}', 400),
            (
                '{"username": "test_username", "email": "test_username@example.com"}',
                400,
            ),
            ('{"username": "test_username", "password": "test_password"}', 400),
            ('{"username": "test_username", "role": "user"}', 400),
            (
                '{"email": "test_username@example.com", "password": "test_password"}',
                400,
            ),
            ('{"email": "test_username@example.com", "role": "user"}', 400),
            ('{"role": "user", "password": "test_password"}', 400),
            (
                '{"username": "test_username", "email": "test_username@example.com", "role": "user"}',
                400,
            ),
            (
                '{"username": "test_username", "email": "test_username@example.com", "password": "test_password", "role": "hacker"}',
                400,
            ),
        ],
    )
    def test_signup_failure(self, payload, excepted_status):
        response = self.client.post(
            "/signup/", data=payload, content_type="application/json"
        )
        assert response.status_code == excepted_status

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "payload, excepted_status",
        [
            (
                {
                    "username": "test_user",
                    "email": "newemail@example.com",
                    "password": "test_password",
                },
                400,
            ),
            (
                {
                    "username": "new_user",
                    "email": "test_user@example.com",
                    "password": "test_password",
                },
                400,
            ),
        ],
    )
    def test_signup_existing_user(self, first_user, payload, excepted_status):
        response = self.client.post(
            "/signup/", data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == excepted_status
