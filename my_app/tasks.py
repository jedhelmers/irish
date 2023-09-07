from celery import Celery
import pika
import json
from . import utils
from celery import shared_task, current_task
from my_app.models import UserQueries
from django.contrib.auth.models import User
from backend.celery import app


try:
    user = User.objects.create(username='dummyuser')
except:
    user = User.objects.get(username='dummyuser')

@shared_task(bind=True)
def handle_translation_and_pronunciation(self, original_text):
    print('Task started...')

    # Call the translation API
    translation_data = utils.fetch_translation(original_text)

    # Call the pronunciation API
    translation_data['pronunciation'] = utils.fetch_ipa(translation_data['targetTransliteration'])['output']

    # Create a new UserQueries object and save it to the database
    if map_to_user_queries(translation_data):
        print('Mapped to UserQueries: Task finished!')

        return {
            "err": translation_data.get('err', None),
            "translation": translation_data.get('result', ''),
            "input": translation_data.get('sourceTransliteration', ''),
            "pronunciation": translation_data.get('pronunciation', '')
        }

    return False


def map_to_user_queries(combined_data):
    global user

    try:
        user_query = UserQueries.objects.create(
            user=user,
            input_text=combined_data.get('sourceTransliteration', ''),
            output_text=combined_data.get('result', ''),
            pronunciation=combined_data.get('pronunciation', '')
        )
        user_query.save()

        return True
    except:
        return False


@app.task
def translate(text):
    # Your logic here to call the translation API
    response = translate_english_to_irish(text)
    result = response.json()

    # Call the pronunciation API here
    pronunciation_result = call_pronunciation_api(result)

    return pronunciation_result


def call_pronunciation_api(translation_result):
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

    print('BUTTS')

    channel.basic_publish(
        exchange='',
        routing_key='translation_queue',
        body=json.dumps(payload)
    )

    connection.close()
