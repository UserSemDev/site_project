import os
import pytest
from django.core.cache import cache
from django.test import Client
from django.core.management import call_command
from testcontainers.postgres import PostgresContainer

# fmt: off
pytest_plugins = [
]


# fmt: on


@pytest.fixture(autouse=True)
def _cache():
    """Clear django cache after each test run."""
    yield
    cache.clear()


postgres = PostgresContainer("postgres:latest")

def pytest_configure():
    postgres.start()
    os.environ["POSTGRES_DB"] = postgres.dbname
    os.environ["POSTGRES_USER"] = postgres.username
    os.environ["POSTGRES_PASSWORD"] = postgres.password
    os.environ["POSTGRES_HOST"] = postgres.get_container_host_ip()
    os.environ["POSTGRES_PORT"] = postgres.get_exposed_port(5432)
    os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

    import django
    django.setup()


def pytest_unconfigure(config):
    postgres.stop()


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def client():
    return Client()
