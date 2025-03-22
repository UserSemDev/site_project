import json

import pytest


@pytest.mark.e2e
def test_end_to_end_flow(client):
    data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test_password",
    }
    response = client.post(
        "/signup/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["jwt"]

    data = {"username": "test_user", "password": "test_password"}
    response = client.post(
        "/signin/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json()["jwt"]

    token = response.json()["jwt"]
    response = client.get("/auth/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
