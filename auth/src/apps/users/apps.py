from django.apps import AppConfig
from mongoengine import connect

from core.settings import MONGO_DB_NAME, MONGO_HOST, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD


class UsersConfig(AppConfig):
    name = "apps.users"

    def ready(self):
        connect(
            db=MONGO_DB_NAME,
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authentication_source="admin"
        )
