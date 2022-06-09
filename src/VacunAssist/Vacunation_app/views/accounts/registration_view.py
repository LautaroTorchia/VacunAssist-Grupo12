from django.shortcuts import redirect, render
from django.urls import reverse
from Vacunation_app.forms.creating_user_form import CreatingPatientForm
from Vacunation_app.custom_functions import check_dni, generate_keycode
from django.contrib import messages

from Vacunation_app.models import CustomUserManager
from Vacunation_app.turn_assignment import TurnAssignerNonRisk, TurnAssignerRisk


def registration_view(request):
    form=CreatingPatientForm(request.POST or None)
    success= False
    data={}
    if 'validar_dni' in request.POST:
        form.errors.clear()
        if form.is_valid():
            success, data = check_dni(form.data["dni"])
            if success:
                messages.success(request,"DNI validado")
            else:
                messages.error(request, data["mensaje de error"])
                form = CreatingPatientForm()
        request.session["data"]=data
    else:
        if form.is_valid():
            user=CustomUserManager()
            clave=generate_keycode()
            nombre=request.session["data"].get("nombre")
            fecha_nac=request.session["data"].get("fecha_nacimiento")
            patient=user.create_patient(
                form.cleaned_data["dni"],form.cleaned_data["password"],
                nombre,fecha_nac,form.cleaned_data["email"],clave,form.cleaned_data["zona"],
                form.cleaned_data["cantidad_dosis_covid"],form.cleaned_data["ultima_gripe"],
                form.cleaned_data["tuvo_amarilla"],form.cleaned_data["es_de_riesgo"]
                )

            if patient.es_de_riesgo:
                assigner=TurnAssignerRisk(patient)
            else:
                assigner=TurnAssignerNonRisk(patient)
            assigner.assign_turns()
                
            messages.success(request, "Cuenta creada Correctamente")
            return redirect(reverse("login"))


    return render(request,"registration/registration.html",{"form":form})