import json

import pytest


@pytest.mark.django_db
def test_create_event_success(client):
    ...

@pytest.mark.django_db
def test_create_event_failure(client, auth_token):
    headers = {"Authorization": "Bearer " + auth_token}
    data = {
        "name": "New Event",
        "description": "Event description",
        "event_date": "2025-06-01T12:00:00Z",
        "available_tickets": 100,
        "ticket_price": 1500.00,
    }
    response = client.post('/events/', data=json.dumps(data), headers=headers)
    assert response.status_code == 403