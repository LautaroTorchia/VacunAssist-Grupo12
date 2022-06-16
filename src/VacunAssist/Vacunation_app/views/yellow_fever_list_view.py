from django.shortcuts import render, redirect
from ..models import Usuario, Paciente
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse


@permission_required("Vacunation_app.Administrador")
@login_required()
def yellow_fever_confirmation_view(request, id):
    user = Usuario.objects.get(id=id)
    patient = Paciente.objects.get(user=user)
    context = {"patient": patient}
    return render(request, "yellow_fever_confirmation.html", context)