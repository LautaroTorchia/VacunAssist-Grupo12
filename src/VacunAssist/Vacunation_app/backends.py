from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


Usuario = get_user_model()
class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Usuario.objects.get(dni=username)
            if user.check_password(password):   
                return user 
            return None
        except Usuario.DoesNotExist:
            return None

        
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None