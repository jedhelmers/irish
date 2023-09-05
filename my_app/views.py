from django.http import JsonResponse
from django.http import HttpResponse
from .models import UserQueries, Tags, Song
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .producer import send_message
import my_app.utils as utils



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