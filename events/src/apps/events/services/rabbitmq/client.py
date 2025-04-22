import json
import os

import pika


class RmqClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv("RABBITMQ_HOST"),
                port=int(os.getenv("RABBITMQ_PORT")),
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_DEFAULT_USER"),
                    os.getenv("RABBITMQ_DEFAULT_PASS"),
                ),
            )
        )
        self.channel = self.connection.channel()

    def send(self, queue_name: str, event_name: str, payload: dict):
        self.channel.queue_declare(queue=queue_name, durable=True)
        message = json.dumps({"event": event_name, "payload": payload})
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
