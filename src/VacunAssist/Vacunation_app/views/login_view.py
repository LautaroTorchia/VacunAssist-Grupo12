from django.contrib.auth.views import LoginView
from ..forms.login_form import LoginForm,LoginClaveForm

class CustomLogin(LoginView):
    authentication_form= LoginForm
    def post(self, request, *args, **kwargs):
        form = self.authentication_form(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)

class CustomLoginClave(LoginView):
    authentication_form= LoginClaveForm
    
    
