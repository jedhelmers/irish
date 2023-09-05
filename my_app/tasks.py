from celery import Celery
import pika
import json
import requests
from . import utils

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def translate(text):
    # Your logic here to call the translation API
    response = translate_english_to_irish(text)
    result = response.json()

    # Call the pronunciation API here
    pronunciation_result = call_pronunciation_api(result)
    print('\npronunciation_result', pronunciation_result)

    return pronunciation_result


def call_pronunciation_api(translation_result):
    print('\ntranslation_result', translation_result)
    result = utils.fetch_ipa('Hello!')


def translate_english_to_irish(english_text):
    # Here goes your actual translation logic.
    # This is a mocked example.
    return f"Translated: {english_text}"


def publish_translation_task(english_text):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='translation_queue')

    payload = {
        'text': english_text
    }

    print('payload', payload)

    channel.basic_publish(
        exchange='',
        routing_key='translation_queue',
        body=json.dumps(payload)
    )

    connection.close()
