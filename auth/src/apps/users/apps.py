from core.settings import (
    MONGO_AUTH_DB,
    MONGO_DB,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USERNAME,
)
from django.apps import AppConfig
from mongoengine import connect


class UsersConfig(AppConfig):
    name = "apps.users"

    def ready(self):
        connect(
            db=MONGO_DB,
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authentication_source=MONGO_AUTH_DB,
        )
