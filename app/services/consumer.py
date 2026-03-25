import time
import json
import pika
import os
from dotenv import load_dotenv
import os
from app.database.mongo import salvar

load_dotenv()



RABBITMQ_URL = os.getenv("RABBITMQ_URL")


class RabbitMqConsumer:
    def __init__(self, filas):
        self.filas = filas
        self.connection = None
        self.channel = None

    def conection(self):
        connection_parameters = pika.URLParameters(RABBITMQ_URL)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

        for fila in self.filas:
            self.channel.queue_declare(queue=fila, durable=True)

        self.channel.basic_qos(prefetch_count=1)

    def callback(self, ch, method, properties, body):
        evento = json.loads(body)
        salvar(evento)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumir(self):
        while True:
            try:
                self.conection()

                for fila in self.filas:
                    self.channel.basic_consume(queue=fila, on_message_callback=self.callback, auto_ack=False)

                self.channel.start_consuming()
            except:
                time.sleep(5)
            finally:
                if self.channel and self.channel.is_open:
                    self.channel.stop_consuming()

if __name__ == "__main__":
    consumer = RabbitMqConsumer(['eventos_queue', 'queue_crud'])
    consumer.consumir()
