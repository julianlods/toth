from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

Usuario = get_user_model()

class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(Q(username=username) | Q(email=username))
        except Usuario.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
