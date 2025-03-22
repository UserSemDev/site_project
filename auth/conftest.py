import pytest
from django.core.cache import cache
from django.test import Client
from mongoengine import connect, disconnect
from testcontainers.mongodb import MongoDbContainer

from apps.users.models import User
from apps.users.utils import generate_jwt

# fmt: off
pytest_plugins = [
]
# fmt: on


@pytest.fixture(autouse=True)
def _cache():
    """Clear django cache after each test run."""
    yield
    cache.clear()


@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo


@pytest.fixture(scope="function", autouse=True)
def clear_db(mongo_container):
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
def client():
    return Client()


@pytest.fixture
def first_user():
    user = User(username="test_user", email="test_user@example.com")
    user.set_password("test_password")
    user.save()
    return user


@pytest.fixture
def auth_token(first_user):
    return generate_jwt(first_user.id)
