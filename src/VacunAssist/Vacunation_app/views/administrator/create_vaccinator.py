from VacunAssist.settings import DEFAULT_FROM_EMAIL
from Vacunation_app.custom_functions import generate_keycode, generate_random_password, get_referer,check_dni
from Vacunation_app.forms.creating_user_form import CreatingVaccinatorForm,EnteringDniForm
from Vacunation_app.models import CustomUserManager
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse


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

    return render(request, "administrator/dni_validation_view.html", {
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

    return render(request, "administrator/vaccinator_creation.html", context)