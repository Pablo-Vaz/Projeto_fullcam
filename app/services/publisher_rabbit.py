import json
import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")


class PublisherRabbitMq:
    def __init__(self, exchange: str, queue: str, type: str, routing_key):
        self.exchange = exchange
        self.queue = queue
        self.type = type
        self.rk = routing_key
        self.connection = None
        self.channel = None

    def init_conn(self):
        connection_parameters = pika.URLParameters(RABBITMQ_URL)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

    def publish(self, evento):
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.type, durable=True
        )
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue, routing_key=self.rk
        )
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.rk,
            body=evento,
            properties=pika.BasicProperties(delivery_mode=2),
        )


evento_rabbit = PublisherRabbitMq(
        "eventos_exchange", "eventos_queue", "fanout", "cameras"
    )
crud_rabbit = PublisherRabbitMq("crud_exchange", "crud_queue", "fanout", "crud")

def get_eventos():
    return evento_rabbit

def get_crud():
    return crud_rabbit