from Vacunation_app.turn_assignment import TurnAssignerNonRisk, TurnAssignerRisk
from Vacunation_app.forms.creating_user_form import CreatingPatientForm
from Vacunation_app.custom_functions import check_dni, generate_keycode, vacunassist_send_mail
from Vacunation_app.models import CustomUserManager
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

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
                form.cleaned_data["ultima_gripe"]=date(1980,1,1)


            nombre=request.session["data"].get("nombre")
            fecha_nac=datetime.strptime(request.session["data"].get("fecha_nacimiento"),'%Y-%m-%dT%H:%M:%S%z')
            patient=user.create_patient(
                form.cleaned_data["dni"],form.cleaned_data["password"],
                nombre,fecha_nac,form.cleaned_data["email"],clave,form.cleaned_data["zona"],
                form.cleaned_data["cantidad_dosis_covid"],form.cleaned_data["ultima_gripe"],
                form.cleaned_data["tuvo_amarilla"],form.cleaned_data["es_de_riesgo"]
                )

            if patient.es_de_riesgo or patient.user.fecha_nac.date()+relativedelta(years=60) >= timezone.now().date():
                assigner=TurnAssignerRisk(patient.user)
            else:
                assigner=TurnAssignerNonRisk(patient.user)
            assigner.assign_turns()
            vacunassist_send_mail('emails/registro_paciente.html',{"clave":clave, "dni":form.cleaned_data["dni"]}
            ,"Registro de vacunador a VacunAssist",form.cleaned_data.get("email"))
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