from django.apps import AppConfig

from apps.events.services.rabbitmq.adapter import LazyRmqSender
from django.conf import settings


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.events"

    def ready(self):
        settings.RMQ_SENDER = LazyRmqSender()
