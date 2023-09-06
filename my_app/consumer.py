import pika
import json
import utils
from my_app.models import UserQueries

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    # Deserialize the JSON object from the message queue
    data = json.loads(body)
    query_text = data.get("query_text", "")

    # Call the translation API
    translation_data = utils.fetch_translation(query_text)

    # Extract the translated text and get its pronunciation
    translated_text = translation_data.get('result', '')
    pronunciation = utils.fetch_ipa(translated_text)

    # Add the pronunciation to the translation data
    translation_data['pronunciation'] = pronunciation

    # Save to the UserQueries model
    UserQueries.objects.create(
        query_text=query_text,
        translated_text=translated_text,
        pronunciation=pronunciation,
        # ... any other fields ...
    )

