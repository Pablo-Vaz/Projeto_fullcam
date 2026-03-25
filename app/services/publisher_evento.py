import json
import pika
import os
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")



def publicar(eventos):
    
    connection_parameters = pika.URLParameters(RABBITMQ_URL)
    
    conection = pika.BlockingConnection(connection_parameters)
    
    channel = conection.channel()

    channel.exchange_declare(exchange="eventos_exchange",exchange_type="fanout", durable=True)

    channel.queue_declare(queue="eventos_queue", durable=True)

    channel.queue_bind(exchange="eventos_exchange", queue="eventos_queue", routing_key="cameras")

    channel.basic_publish(exchange="eventos_exchange", routing_key="cameras", body=eventos , properties=pika.BasicProperties(delivery_mode=2))


    conection.close()

if __name__ == "__main__":
    publicar()