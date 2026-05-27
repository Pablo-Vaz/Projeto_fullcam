import time
import json
import pika
import os
from dotenv import load_dotenv
from app.database.mongo import salvar

load_dotenv()


RABBITMQ_URL = os.getenv("RABBITMQ_URL")


class ConsumerConn:
    def __init__(self):
        self.connection = None
        self.channel = None

    def conection(self):
        connection_parameters = pika.URLParameters(RABBITMQ_URL)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

        return self.channel


class ConsumerQueue:
    def __init__(self, channel, queue):
        self.queue = queue
        self.channel = channel

    def queue_declare(self):
        for queue in self.queue:
            self.channel.queue_declare(queue=queue, durable=True)

        self.channel.basic_qos(prefetch_count=1)


class Consumer:
    def __init__(self, channel, queue):
        self.queue = queue
        self.channel = channel

    @staticmethod
    def callback(ch, method, properties, body):
        evento = json.loads(body)
        salvar(evento)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumir(self):
        while True:
            try:
                for queue in self.queue:
                    self.channel.basic_consume(
                        queue=queue, on_message_callback=self.callback, auto_ack=False
                    )
                self.channel.start_consuming()
            except:
                time.sleep(5)
            


if __name__ == "__main__":
    conn = ConsumerConn()
    channel = conn.conection()

    setup = ConsumerQueue(channel, ["eventos_queue", "crud_queue"])

    setup.queue_declare()

    consumer = Consumer(channel, ["eventos_queue", "crud_queue"])
    consumer.consumir()
