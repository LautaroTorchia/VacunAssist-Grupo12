from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model


Usuario = get_user_model()
class UsuarioBackend(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = Usuario.objects.get(dni=username)
            if user.clave == password:   
                return user 
            return None
        except Usuario.DoesNotExist:
            return None

        
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None