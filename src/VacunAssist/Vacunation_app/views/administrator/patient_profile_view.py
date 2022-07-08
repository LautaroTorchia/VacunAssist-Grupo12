from django.shortcuts import render, redirect
from Vacunation_app.models import Paciente, Usuario
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse


@permission_required("Vacunation_app.Administrador")
@login_required()
def patient_profile_view(request,id):
    user = Usuario.objects.get(id=id)
    patient = Paciente.objects.get(user=user)
    context = {"patient": patient}
    return render(request, "administrator/patient_profile.html", context)