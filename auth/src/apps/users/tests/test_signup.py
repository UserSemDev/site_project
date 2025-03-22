import json

import pytest


@pytest.mark.unit
def test_signup_success(client):
    data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "test_password",
    }

    response = client.post(
        "/signup/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["jwt"]


@pytest.mark.unit
@pytest.mark.parametrize(
    "payload, excepted_status",
    [
        ({}, 400),
        ("{broken_json", 400),
        ({"username": "test_username"}, 400),
        ({"email": "test_username@example.com"}, 400),
        ({"password": "test_password"}, 400),
        ({"role": "user"}, 400),
        (
            {"username": "test_username", "email": "test_username@example.com"},
            400,
        ),
        ({"username": "test_username", "password": "test_password"}, 400),
        ({"username": "test_username", "role": "user"}, 400),
        (
            {"email": "test_username@example.com", "password": "test_password"},
            400,
        ),
        ({"email": "test_username@example.com", "role": "user"}, 400),
        ({"role": "user", "password": "test_password"}, 400),
        (
            {
                "username": "test_username",
                "email": "test_username@example.com",
                "role": "user",
            },
            400,
        ),
        (
            {
                "username": "test_username",
                "email": "test_username@example.com",
                "password": "test_password",
                "role": "hacker",
            },
            400,
        ),
    ],
)
def test_signup_failure(client, payload, excepted_status):
    if isinstance(payload, str):
        data = payload
    else:
        data = json.dumps(payload)
    response = client.post("/signup/", data=data, content_type="application/json")
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
def test_signup_existing_user(client, first_user, payload, excepted_status):
    response = client.post(
        "/signup/", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == excepted_status
