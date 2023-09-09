from celery import Celery
import pika
import json
from . import utils
from celery import shared_task, current_task
from my_app.models import UserQueries, Tags
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from backend.celery import app

try:
    butts = User.objects.create(username='dummyuser')
except:
    butts = User.objects.get(username='dummyuser')


@shared_task
def handle_guesses(query_id, guess):
    user_query = UserQueries.objects.get(pk=query_id)

    if user_query:
        is_correct = user_query.output_text.lower() == guess.lower() or user_query.input_text.lower() == guess.lower()

        if (is_correct):
            user_query.correct_answers += 1
        else:
            user_query.incorrect_answers += 1

        user_query.save()

        return is_correct

    return False


@shared_task(bind=True)
def handle_translation_and_pronunciation(self, original_text):
    print('Task started...')

    # Call the translation API
    translation_data = utils.fetch_translation(original_text)

    # Call the pronunciation API
    translation_data['pronunciation'] = utils.fetch_ipa(translation_data['targetTransliteration'])['output']

    # Create a new UserQueries object and save it to the database
    row = map_to_user_queries(translation_data)
    if row:
        print('Mapped to UserQueries: Task finished!', row)

        return {
            "queryID": row.id,
            "err": translation_data.get('err', None),
            "translation": translation_data.get('result', ''),
            "input": translation_data.get('sourceTransliteration', ''),
            "pronunciation": translation_data.get('pronunciation', '')
        }

    return False


@shared_task
def handle_add_tags_to_userquery(query_id, tags):
    try:
        query = get_object_or_404(UserQueries, id=query_id)

        for tag_name in tags:
            tag, created = Tags.objects.get_or_create(tag=tag_name)
            query.tags.add(tag)

            query.save()

        return True
    except:
        return False

def map_to_user_queries(combined_data):
    global butts

    try:
        user_query = UserQueries.objects.create(
            user=butts,
            input_text=combined_data.get('sourceTransliteration', ''),
            output_text=combined_data.get('result', ''),
            pronunciation=combined_data.get('pronunciation', '')
        )
        
        user_query.save()
        print('ID', user_query.id)

        return user_query
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

    channel.basic_publish(
        exchange='',
        routing_key='translation_queue',
        body=json.dumps(payload)
    )

    connection.close()
