from django.contrib.auth.models import User

class UserCreationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if cookie exists
        irish_user_id = request.COOKIES.get('irish_user_id')

        if not irish_user_id:
            # Create a new user
            try:
                user = User.objects.create_user(username="dummyuser")
                irish_user_id = user.id
            except:
                user = User.objects.get(username='dummyuser')
                irish_user_id = user.id

        response = self.get_response(request)

        # Set the cookie if it doesn't exist
        if not request.COOKIES.get('irish_user_id'):
            response.set_cookie('irish_user_id', irish_user_id)

        return response
