from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model,login, authenticate
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse
from Vacunation_app.forms.login_form import LoginForm, LoginClaveForm
from Vacunation_app.custom_functions import get_referer
from Vacunation_app.models import Paciente
from Vacunation_app.turn_assignment import TurnAssigner

#TODO: Usar isvalid para los datos como en cambiarNombre
Usuario = get_user_model()


class CustomLogin(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    next_page = "accounts/loginClave/"

    def get(self, request, *args, **kwargs):
        request.session["dni_validated"]=False
        request.session["next"]=request.GET.get("next")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance_form = self.get_form(form_class=self.authentication_form)
        instance_form.is_valid()
        dni_o_mail = instance_form.cleaned_data["dni_o_mail"]
        password = instance_form.cleaned_data["contraseña"]
        try:
            user = Usuario.objects.get(dni=dni_o_mail)
        except ObjectDoesNotExist:
            try:
                user = Usuario.objects.get(email=dni_o_mail)
            except ObjectDoesNotExist:
                messages.error(self.request, "Usuario no registrado")
                return redirect(reverse("login"))
        if check_password(password, user.password):
            request.session['dni'] = user.dni
            return redirect(reverse("loginClave"))
        else:
            messages.error(self.request, "Contraseña incorrecta")
            return redirect(reverse("login"))


class CustomLoginClave(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginClaveForm

    def post(self, request, *args, **kwargs):
        instance_form = self.get_form(form_class=self.authentication_form)
        instance_form.is_valid()
        clave = instance_form.cleaned_data["clave"]
        dni = request.session['dni']
        user = authenticate(request, username=dni, password=clave)
        if user is not None:
            login(request, user)
            if user.has_perm("Vacunation_app.Paciente") and not user.has_perm("Vacunation_app.Administrador"):
                paciente=Paciente.objects.get(user=request.user)
                assigner=TurnAssigner.get_assigner(paciente)
                assigner.assign_gripe_turn()
            try:
                if request.session["next"]:
                    return redirect(request.session.get("next"))
            except:
                pass
            return redirect("/")
        else:
            messages.error(self.request, "Código incorrecto")
            return redirect(reverse("loginClave"))

    def get(self, request, *args, **kwargs):
        if not get_referer(request):
            return redirect(reverse("login"))
        return LoginView.get(self, request, args, kwargs)
