import random
import string
from django.views.generic.edit import FormView
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from Vacunation_app.forms.stock_form import StockForm
from Vacunation_app.forms.update_name_form import NameUpdateForm
from Vacunation_app.custom_functions import check_dni, get_referer
from Vacunation_app.forms.creating_user_form import CreatingVaccinatorForm, EnteringDniForm
from Vacunation_app.models import VacunaEnVacunatorio, Vacunador, Vacunatorio, CustomUserManager
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def administrator_home_view(request):
    if "logout" in request.POST:
        logout(request)
        return redirect(reverse("login"))
    return render(request, "administrator/administrator_view.html", {})


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def validating_dni_for_vaccinator_view(request):

    dni_form = EnteringDniForm(request.POST or None)
    success = False
    data = {}

    if dni_form.is_valid():
        dni_to_validate = dni_form.cleaned_data.get("dni")
        success, data = check_dni(dni_to_validate)
        if success:
            request.session['dni_to_create'] = dni_to_validate
            request.session['fecha_to_create'] = data["fecha_nacimiento"]
            request.session['nombre_to_create'] = data["nombre"]
            return redirect(reverse("create_vaccinator_step2"))
        else:
            messages.error(request, data["mensaje de error"])
            dni_form = EnteringDniForm()

    return render(request, "dni_validation_view.html", {
        "form": dni_form,
    })


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def creating_vaccinator_view(request):
    if not get_referer(request):
        return redirect(reverse("create_vaccinator"))

    letters = string.ascii_lowercase
    numbers = string.digits
    user_creation_form = CreatingVaccinatorForm(request.POST or None)

    if user_creation_form.is_valid():
        user_instance = user_creation_form.save(commit=False)
        vaccinator = CustomUserManager()
        password = ''.join(random.choice(letters) for i in range(10))
        clave = ''.join(random.choice(numbers) for i in range(4))
        user_instance = vaccinator.create_vaccinator(
            request.session["dni_to_create"], password,
            request.session["nombre_to_create"],
            request.session["fecha_to_create"], user_instance.email, clave,
            user_instance.zona)
        user_creation_form = CreatingVaccinatorForm()

        send_mail("Registro de vacunador a VacunAssist",
                  f"""Hola, {user_instance.nombre_completo}
        Se ha registrado una cuenta en VacunAssist a su nombre aqui estan sus credenciales: 
        Contraseña: {password}
        clave:   {user_instance.clave}""",
                  DEFAULT_FROM_EMAIL, [user_instance.email],
                  fail_silently=False)
        messages.success(request, "Cuenta creada Correctamente")
        return redirect(reverse("creating-vaccinator-view"))


    context = {
        "form": user_creation_form,
        "DNI": request.session["dni_to_create"],
        "nombre": request.session["nombre_to_create"],
    }

    return render(request, "vaccinator_creation.html", context)


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def stock_view(request):

    vaccine_info = VacunaEnVacunatorio.objects.all()
    vaccination_center_info = Vacunatorio.objects.all()
    stock_form = StockForm(request.POST or None)

    if stock_form.is_valid():

        vacuna = stock_form.cleaned_data.get("vacuna")
        vacunatorio = stock_form.cleaned_data.get("vacunatorio")

        vacunation_to_update = VacunaEnVacunatorio.objects.get(
            vacuna=vacuna, vacunatorio=vacunatorio)
        vacunation_to_update.stock += stock_form.cleaned_data.get("stock")
        vacunation_to_update.save()
        messages.success(request,"Stock actualizado")
        stock_form = StockForm()

    context = {
        "vaccine_info": vaccine_info,
        "vaccination_center_info": vaccination_center_info,
        "stock_form": stock_form,
    }
    return render(request, "stock_view.html", context)


class NameUpdate(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form = NameUpdateForm
    template_name = "vacunatorio_name_update.html"
    permission_required = ("Vacunation_app.Administrador", )
    raise_exception = True

    def post(self, request, *args, **kwargs):
        instance_form = self.get_form(form_class=self.form)
        instance_form.is_valid()
        vacunatorio = instance_form.cleaned_data["nombre_actual"]
        nombre_nuevo = instance_form.cleaned_data["nombre_nuevo"]
        try:
            Vacunatorio.objects.get(nombre=nombre_nuevo)
            messages.error(self.request, "Nombre de vacunatorio en uso")
        except Vacunatorio.DoesNotExist:
            vacunatorio.nombre = nombre_nuevo
            vacunatorio.save()
            messages.success(self.request,
                             f"Vacunatorio cambiado a: {vacunatorio.nombre}")
        return redirect("/administrator/change_name/")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form})
