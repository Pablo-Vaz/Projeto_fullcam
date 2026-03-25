import time
import json
import pika
import os
from dotenv import load_dotenv
import os
from app.database.mongo import salvar

load_dotenv()



RABBITMQ_URL = os.getenv("RABBITMQ_URL")


def consumir():
    while True:
        try:
            connection_parameters = pika.URLParameters(RABBITMQ_URL)
            
            channel = pika.BlockingConnection(connection_parameters).channel()

            channel.queue_declare(queue='eventos_queue', durable=True)
            channel.queue_declare(queue='queue_crud', durable=True)

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(queue='eventos_queue', on_message_callback=callback, auto_ack=False)
            channel.basic_consume(queue='queue_crud', on_message_callback=callback, auto_ack=False)

            channel.start_consuming()
        except:
            time.sleep(5)
            continue

def callback(ch, method, properties, body):
    
    evento = json.loads(body)
    salvar(evento)
    ch.basic_ack(delivery_tag=method.delivery_tag)
       


if __name__ == "__main__":
    consumir()
