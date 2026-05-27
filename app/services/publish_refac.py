import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")


class RabbitConn:
    def __init__(self):
        self.connection = None
        self.channel = None

    def init_conn(self):
        connection_parameters = pika.URLParameters(RABBITMQ_URL)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()


class PublisherRabbitMq:
    def __init__(
        self, channel, exchange: str, queue: str, type: str, routing_key: str
    ):
        self.exchange = exchange
        self.queue = queue
        self.type = type
        self.routing_key = routing_key
        self.channel = channel

    def publish(self, evento):
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.type, durable=True
        )
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue, routing_key=self.routing_key
        )
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=evento,
            properties=pika.BasicProperties(delivery_mode=2),
        )


def get_eventos():
    conn = RabbitConn()
    conn.init_conn()
    publish = PublisherRabbitMq(
        conn.channel, "eventos_exchange", "eventos_queue", "fanout", "cameras"
    )

    return publish


def get_crud():
    conn = RabbitConn()
    conn.init_conn()
    publish = PublisherRabbitMq(
        conn.channel, "crud_exchange", "crud_queue", "fanout", "crud"
    )

    return publish
