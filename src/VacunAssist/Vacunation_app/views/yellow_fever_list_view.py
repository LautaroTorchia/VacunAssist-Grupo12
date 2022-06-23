from django.shortcuts import render, redirect
from ..models import listaDeEsperaFiebreAmarilla, Turno
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from Vacunation_app.forms.yellow_fever_turn_form import assigningYellowFeverTurn
from Vacunation_app.turn_assignment import TurnAssignerYellowFever
import datetime
from django.contrib import messages


@permission_required("Vacunation_app.Administrador")
@login_required()
def yellow_fever_confirmation_view(request, id):
    petition = listaDeEsperaFiebreAmarilla.objects.get(id=id)
    form=assigningYellowFeverTurn(request.POST or None)
    if form.is_valid():
        fecha=datetime.datetime.combine(form.cleaned_data["fecha_del_turno"],form.cleaned_data["hora_del_turno"])
        try:
            if Turno.objects.get(fecha=fecha):
                messages.error(request,"Esa fecha y hora ya tiene un turno registrado, asigne otra fecha")
        except:
            TurnAssignerYellowFever(petition.paciente).assign_yellow_fever_turn(fecha,petition.vacunatorio)
            messages.success(request,f"turno asignado con exito en {fecha}")
            petition.delete()
            return redirect(reverse("yellow_fever_list"))
    context = {"petition": petition, "form":form}
    return render(request, "yellow_fever_confirmation.html", context)

@permission_required("Vacunation_app.Administrador")
@login_required()
def reject_petition_view(request,id):
    petition = listaDeEsperaFiebreAmarilla.objects.get(id=id)
    messages.success(request,"Turno rechazado")
    petition.delete()
    return redirect(reverse("yellow_fever_list"))