import random
import string
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from Vacunation_app.custom_functions import check_dni, generate_keycode, generate_random_password, get_referer
from Vacunation_app.forms.creating_user_form import CreatingVaccinatorForm, EnteringDniForm
from Vacunation_app.models import VacunaEnVacunatorio, Vacunador, Vacunatorio, CustomUserManager, Paciente, listaDeEsperaFiebreAmarilla
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
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

    user_creation_form = CreatingVaccinatorForm(request.POST or None)

    if user_creation_form.is_valid():
        user_instance = user_creation_form.save(commit=False)
        vaccinator = CustomUserManager()
        password = generate_random_password()
        clave = generate_keycode()
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
def patients_list_view(request):
    queryset = Paciente.objects.all()
    context = {"object_list": queryset}
    return render(request, "patients_list.html", context)

@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def yellow_fever_list_view(request):
    print("-"*50)
    queryset = listaDeEsperaFiebreAmarilla.objects.all()
    print(queryset,"-"*50)
    context = {"object_list": queryset}
    return render(request, "yellow_fever_list.html", context)