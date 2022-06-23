from datetime import date
from django.shortcuts import redirect, render
from django.urls import reverse
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from Vacunation_app.forms.creating_user_form import CreatingPatientForm
from Vacunation_app.custom_functions import check_dni, generate_keycode
from django.contrib import messages
from django.core.mail import send_mail
from Vacunation_app.models import CustomUserManager
from Vacunation_app.turn_assignment import TurnAssignerNonRisk, TurnAssignerRisk
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def registration_view(request):
    form=CreatingPatientForm(request.POST or None)
    success= False
    data={}
    if 'validar_dni' in request.POST:
        form.errors.clear()
        if form.is_valid():
            success, data = check_dni(form.data["dni"])
            if success:
                request.session["dni_validated"]=True
                messages.success(request,"DNI validado")
            else:
                request.session["dni_validated"]=False
                messages.error(request, data["mensaje de error"])

        request.session["data"]=data
    else:
        if form.is_valid():
            user=CustomUserManager()
            clave=generate_keycode()
            if not form.cleaned_data.get("tiene_gripe"):
                form.cleaned_data["ultima_gripe"]=date(1990,1,1)

            nombre=request.session["data"].get("nombre")
            fecha_nac=request.session["data"].get("fecha_nacimiento")
            print(form.cleaned_data.get("ultima_gripe"))
            patient=user.create_patient(
                form.cleaned_data["dni"],form.cleaned_data["password"],
                nombre,fecha_nac,form.cleaned_data["email"],clave,form.cleaned_data["zona"],
                form.cleaned_data["cantidad_dosis_covid"],form.cleaned_data["ultima_gripe"],
                form.cleaned_data["tuvo_amarilla"],form.cleaned_data["es_de_riesgo"]
                )

            if patient.es_de_riesgo:
                assigner=TurnAssignerRisk(patient.user)
            else:
                assigner=TurnAssignerNonRisk(patient.user)
            assigner.assign_turns()

            html_message = render_to_string('emails/registro_paciente.html', 
            {"clave":clave, "dni":form.cleaned_data["dni"]})
            send_mail("Registro de vacunador a VacunAssist",strip_tags(html_message),from_email=DEFAULT_FROM_EMAIL,recipient_list=[form.cleaned_data["email"]],
            fail_silently=False,html_message=html_message)
            request.session["dni_validated"]=False
            messages.success(request, f"Su clave de autenticación es {clave}")
            messages.success(request, "Cuenta creada Correctamente")
            return redirect(reverse("login"))
    try:
        context={
            "form":form,
            "dni_validated":request.session["dni_validated"] or False}
    except:
        context={
            "form":form,
            "dni_validated":False}
    return render(request,"registration/registration.html",context)