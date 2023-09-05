import pika
import json

def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

    channel = connection.channel()
    channel.queue_declare(queue='song_queue')
    channel.basic_publish(exchange='', routing_key='song_queue', body=json.dumps(message))
    connection.close()
