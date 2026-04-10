from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AuthService:
    """
    Abstraction layer for Authentication.
    Currently uses Django's local User model, but designed to be easily swapped
    with an external AuthManager microservice (e.g., using 'requests' library).
    """

    @staticmethod
    def login_user(request, username, password):
        # Future: response = requests.post(AUTH_MANAGER_URL + '/login', json={'user': username, 'pass': password})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return True, user
        return False, None

    @staticmethod
    def logout_user(request):
        # Future: requests.post(AUTH_MANAGER_URL + '/logout', headers={'Authorization': 'Bearer ...'})
        django_logout(request)

    @staticmethod
    def register_user(username, email, password):
        # Future: response = requests.post(AUTH_MANAGER_URL + '/register', json={'user': username, 'email': email, 'pass': password})
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
