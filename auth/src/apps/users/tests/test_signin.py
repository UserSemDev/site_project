import json

import pytest


@pytest.mark.unit
def test_signin_success(client, first_user):
    data = {"username": "test_user", "password": "test_password"}
    response = client.post(
        "/signin/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json()["jwt"]


@pytest.mark.unit
@pytest.mark.parametrize(
    "payload, excepted_status",
    [
        ({}, 400),
        ("{broken_json}", 400),
        ({"username": "test_user"}, 400),
        ({"password": "test_password"}, 400),
        ({"username": "wrong_username", "password": "test_password"}, 401),
        ({"username": "test_user", "password": "wrong_password"}, 401),
    ],
)
def test_signin_failure(client, first_user, payload, excepted_status):
    if isinstance(payload, str):
        data = payload
    else:
        data = json.dumps(payload)
    response = client.post("/signin/", data=data, content_type="application/json")
    assert response.status_code == excepted_status
