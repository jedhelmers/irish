from django.http import JsonResponse
from django.core.cache import cache
from django.http import HttpResponse
from .models import UserQueries, Tags
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
import uuid
import my_app.utils as utils
import my_app.tasks as tasks
from .tasks import publish_translation_task
import requests

task_id = 0

global_cache = {}


def grafana_proxy(request):
    grafana_url = "http://localhost:3001"  # URL where Grafana is running
    print('grafana_url', grafana_url)

    # Forward the request to Grafana
    response = requests.get(f"{grafana_url}{request.path}", headers=request.headers)
    print('response', response)

    # Return the response from Grafana
    return HttpResponse(response.content, status=response.status_code)


class CustomTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.create_user_id()
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('user_id', context['user_id'])
        return response

    def create_user_id(self):
        return str(uuid.uuid4())


@csrf_exempt
def translate_view(request):
    global task_id
    print('START REQUEST')
    if request.method == 'POST':
        data = json.loads(request.body)
        english_text = data.get('query', '')

        # Make sure text is not empty
        if not english_text:
            return JsonResponse({"error": "No text provided"}, status=400)

        # Use Celery to asynchronously handle the translation and pronunciation
        result = tasks.handle_translation_and_pronunciation(english_text)
        print('result', result)

        return JsonResponse({"status": f'Translation and pronunciation of "{english_text}": Done', "task": json.JSONEncoder().encode(result)})

    return JsonResponse({'error': 'Invalid request'}, status=400)


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


@csrf_exempt
@require_POST
def submit_guess(request):
    if request.method == "POST":
        data = json.loads(request.body)
        guess = data.get("guess", "")
        query_id = data.get('query_id', None)

        # Use Celery to asynchronously handle the translation and pronunciation
        result = tasks.handle_guesses(query_id, guess)
        print('result', result)

        if result:
            return JsonResponse({"message": "Guess recorded!", "isCorrect": result}, status=200)
        else:
            return JsonResponse({"message": "Guess recorded!", "isCorrect": result}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
@require_POST
def add_tags_to_userquery(request, query_id):
    # query = get_object_or_404(UserQueries, id=query_id)
    data = json.loads(request.body)
    tags = data.get('tags', [])
    
    if tasks.handle_add_tags_to_userquery(query_id, tags):
        return JsonResponse({"status": "success", "message": "Tags added successfully"})

    return JsonResponse({'status': 'error', 'message': 'Invalid input'}, status=400)


@require_POST
def remove_tags_from_userquery(request, query_id):
    query = get_object_or_404(UserQueries, id=query_id)
    
    tags = request.POST.getlist('tags')
    for tag_name in tags:
        try:
            tag = Tags.objects.get(tag=tag_name)
            query.tags.remove(tag)
        except Tags.DoesNotExist:
            pass

    return JsonResponse({"status": "success", "message": "Tags removed successfully"})


@csrf_exempt
def remove_userquery(request, query_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    try:
        query = get_object_or_404(UserQueries, id=query_id)
        query.delete()

        return JsonResponse({"status": "success", "message": "UserQuery deleted successfully"})
    except Exception as e:
        return JsonResponse({"status": "fail", "message": "Query not found."})


def get_all_tags(request):
    tags = Tags.objects.all()
    tags_list = [tag.tag for tag in tags]
    return JsonResponse(tags_list, safe=False)


@csrf_exempt
@require_POST
def get_userqueries(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    try:
        data = json.loads(request.body)
        tag_filter = data.get('tags', [])
        print('tag_filter', tag_filter)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON body")

    if tag_filter:
        userqueries = UserQueries.objects.filter(user=user, tags__tag__in=tag_filter).distinct()
    else:
        userqueries = UserQueries.objects.filter(user=user)

    # Convert queries to a list of dictionaries for JSON serialization
    queries_list = [
        {
            "id": query.id, 
            "input_text": query.input_text, 
            "output_text": query.output_text, 
            "pronunciation": query.pronunciation
        } 
        for query in userqueries
    ]

    return JsonResponse(queries_list, safe=False)


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
