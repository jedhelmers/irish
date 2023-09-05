from django.http import JsonResponse
from django.http import HttpResponse

from .models import Song
from .producer import send_message  # Assuming you'll put producer code in the same app

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
    print('\n\nBUTTS', request)
    all_songs = Song.objects.all()
    print('\n\nBUTTS', all_songs)
    # Print the details of each song to the console
    for song in all_songs:
        print(f"User ID: {song}")

    # Also send a simple HTTP response to indicate that the function executed
    return HttpResponse("Query executed, check console.")