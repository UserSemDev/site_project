from abc import ABC, abstractmethod
from typing import Any

from django.utils.functional import LazyObject

from apps.events.services.rabbitmq.client import RmqClient


class AbstractRmqSender(ABC):
    @abstractmethod
    def send_event(self, event_name: str, payload):
        pass


class RmqAdapter(AbstractRmqSender):
    def __init__(self, rmq_client: RmqClient):
        self._rmq_client = rmq_client

    def send_event(self, event_name: str, payload: Any):
        self._rmq_client.send(
            queue_name="queue", event_name=event_name, payload=payload
        )


class LazyRmqSender(LazyObject):
    def _setup(self):
        self._wrapped = RmqAdapter(RmqClient())
