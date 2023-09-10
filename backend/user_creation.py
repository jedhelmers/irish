from django.contrib.auth.models import User
from django.db import transaction
import uuid

class UserCreationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if cookie exists
        irish_user_id = request.COOKIES.get('irish_user_id')

        if not irish_user_id:
            with transaction.atomic():
                try:
                    user = User.objects.create_user(username=uuid.uuid4())
                    irish_user_id = user.id
                except:
                    user = User.objects.get(username=uuid.uuid4())
                    irish_user_id = user.id

        response = self.get_response(request)

        # Set the cookie if it doesn't exist
        if not request.COOKIES.get('irish_user_id'):
            response.set_cookie('irish_user_id', irish_user_id)

        return response
