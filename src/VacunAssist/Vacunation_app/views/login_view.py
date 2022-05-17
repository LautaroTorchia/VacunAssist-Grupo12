from django.contrib.auth.views import LoginView
from ..forms.login_form import LoginForm,LoginClaveForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import Http404




Usuario = get_user_model()
class CustomLogin(LoginView):
    template_name="registration/login.html"
    authentication_form= LoginForm
    next_page="accounts/loginClave/"
    
    def post(self, request, *args, **kwargs):
        dni_o_mail = request.POST['dni_o_mail']
        password = request.POST['contraseña']
        try:
            user = Usuario.objects.get(dni=dni_o_mail)
        except ObjectDoesNotExist:
            try:
                user = Usuario.objects.get(email=dni_o_mail)
            except ObjectDoesNotExist:
                messages.error(self.request,"Usuario no existe")
                return redirect("/accounts/login/")
        if check_password(password,user.password):
            request.session['dni'] = user.dni
            return redirect(f"/accounts/loginClave/")
        else:
            messages.error(self.request,"Contraseña incorrecta")
            return redirect("/accounts/login/")
    
def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

class CustomLoginClave(LoginView):
    authentication_form= LoginClaveForm
    def post(self, request, *args, **kwargs):
        clave=request.POST['clave']
        dni = request.session['dni']
        user = authenticate(request, username=dni,password=clave)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(self.request,"Clave inválda")
            return redirect(f"/accounts/loginClave/")
    
    def get(self, request, *args, **kwargs):
        if not get_referer(request):
            raise Http404
        return LoginView.get(self,request,args,kwargs)

