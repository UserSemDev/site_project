import datetime

import pytest
import pytz
from freezegun import freeze_time

from core.settings import TIME_ZONE


@pytest.mark.unit
def test_auth_success(client, auth_token, first_user):
    headers = {"Authorization": "Bearer " + auth_token}
    response = client.get("/auth/", headers=headers)
    assert response.status_code == 200
    assert response.json()["user"]["username"] == first_user.username


@pytest.mark.unit
@pytest.mark.parametrize(
    "token, expected_status",
    [
        ("invalid_token", 401),
        (None, 403),
    ],
)
def test_auth_failure(client, token, expected_status):
    if token is None:
        headers = {}
    else:
        headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/", headers=headers)
    assert response.status_code == expected_status


@pytest.mark.unit
def test_expired_token(client, auth_token):
    start_time = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    with freeze_time(
        start_time + datetime.timedelta(hours=1) + datetime.timedelta(seconds=5)
    ):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/auth/", headers=headers)
        assert response.status_code == 401
