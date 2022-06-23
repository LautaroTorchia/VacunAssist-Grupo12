from django.shortcuts import render, redirect
from ..models import listaDeEsperaFiebreAmarilla
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from Vacunation_app.forms.yellow_fever_turn_form import assigningYellowFeverTurn


@permission_required("Vacunation_app.Administrador")
@login_required()
def yellow_fever_confirmation_view(request, id):
    turn = listaDeEsperaFiebreAmarilla.objects.get(id=id)
    form=assigningYellowFeverTurn(request.POST or None)
    context = {"turn": turn,"form":form}
    return render(request, "yellow_fever_confirmation.html", context)