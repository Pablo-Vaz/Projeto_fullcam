import json
import pika
import os
from dotenv import load_dotenv
load_dotenv()

RABBITMQ_URL = os.getenv('RABBITMQ_URL')


def publicar_crud(evento):

    connection_parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='exchange_crud', exchange_type='fanout', durable=True)
    channel.queue_declare(queue='queue_crud', durable=True)
    channel.queue_bind(exchange='exchange_crud', queue='queue_crud', routing_key='crud')

    channel.basic_publish(exchange='exchange_crud', routing_key='crud', body=json.dumps(evento, ensure_ascii=False), properties=pika.BasicProperties(delivery_mode=2))

    connection.close()


if __name__ == "__main__":
    publicar_crud()