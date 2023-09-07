from django.http import JsonResponse
from django.core.cache import cache
from django.http import HttpResponse
from .models import UserQueries, Tags, Song
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import time
from celery.result import AsyncResult

from .producer import send_message
import my_app.utils as utils
import my_app.tasks as tasks


from .tasks import publish_translation_task, translate

@csrf_exempt
def translate_view(request):
    print('START REQUEST')
    if request.method == 'POST':
        data = json.loads(request.body)
        english_text = data.get('query', '')

        # Make sure text is not empty
        if not english_text:
            return JsonResponse({"error": "No text provided"}, status=400)

        # Use Celery to asynchronously handle the translation and pronunciation
        result = tasks.handle_translation_and_pronunciation.delay(english_text)

        # POLL THE TASK
        # while True:
        #     result = AsyncResult(result.id)
        #     print(result.status)
        #     if result.status == 'SUCCESS' or result.status == 'FAILURE':
        #         break
        #     time.sleep(1)

        print('result', result)
        if result.ready():
            actual_result = result.get()
            print('actual_result', actual_result)


        return JsonResponse({"status": f'Translation and pronunciation of "{english_text}" in progress', "task_id": result.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def test(test_string):
    print('WEEEE')
    print(test_string)


# @csrf_exempt
# def check_task_status(request, task_id):
#     task_result = AsyncResult(task_id)

#     print('task_result', task_result)
#     print('task_result', task_result.ready())

#     if task_result.ready():
#         return JsonResponse({"status": "finished", "result": task_result.get()})
#     else:
#         return JsonResponse({"status": "pending"})

def check_task_status(request, task_id):
    status = cache.get(f"task_{task_id}_status", "pending")
    print('STATUS', status)
    return JsonResponse({"status": status})



@csrf_exempt
def translate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data\n', data)
        english_text = data.get('query', '')
        print('english_text\n', english_text)
        # english_text = data.get('query', '')

        publish_translation_task(english_text)

        return JsonResponse({
            'status': 'queued',
            'query': english_text
        })

        # Simulate translation logic, ideally you should use a translation API or library here
        irish_translation = utils.fetch_translation(english_text)

        irish_translation['pronunciation'] = utils.fetch_ipa(irish_translation['result'])['output']

        print('\n\nBOOOM!', irish_translation, '\n\n')

        # TODO: Integrate RabbitMQ here for background processing if needed

        return JsonResponse({'translation': irish_translation})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Function to push data to RabbitMQ, call translation and pronunciation APIs, etc.
# This function would probably be more complex in your real application
def process_query(input_text):
    # Mock translation and pronunciation
    output_text = "Translated " + input_text
    pronunciation = "Pronunciation of " + input_text
    return output_text, pronunciation


@method_decorator(login_required, name='dispatch')
class QueryView(View):
    def post(self, request, *args, **kwargs):
        input_text = request.POST.get('input_text', None)
        tag_ids = request.POST.getlist('tag_ids', [])  # Get multiple tag IDs

        if input_text:
            output_text, pronunciation = process_query(input_text)
            query = UserQueries.objects.create(
                user=request.user,
                input_text=input_text,
                output_text=output_text,
                pronunciation=pronunciation,
            )
            query.tags.add(*tag_ids)
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid input'}, status=400)


def create_song(request, user_id):
    print(request)
    notes = [
        [1, 0, 0, 1],
        [0, 1, 0, 0],
        # ... add more arrays
    ]
    message = {
        "user_id": user_id,
        "notes": notes
    }
    send_message(message)  # Send to RabbitMQ
    return JsonResponse({"status": "Message sent to RabbitMQ"})


def query_songs(request):
    # Query all songs in the Song table
    # Test
    print(utils.fetch_ipa('Is i Londain priomhchathair'))
    print('\n\nBUTTS', request)
    all_songs = Song.objects.all()
    print('\n\nBUTTS', all_songs)
    # Print the details of each song to the console
    for song in all_songs:
        print(f"User ID: {song}")

    # Also send a simple HTTP response to indicate that the function executed
    return HttpResponse("Query executed, check console.")