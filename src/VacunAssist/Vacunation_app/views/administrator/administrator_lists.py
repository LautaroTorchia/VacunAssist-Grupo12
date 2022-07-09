from django.shortcuts import redirect
from django.urls import  reverse_lazy
from Vacunation_app.custom_functions import AbstractAdminListView
from Vacunation_app.models import Vacunador, Paciente, listaDeEsperaFiebreAmarilla, listaDeEsperaCovid
from typing import Any
from django.http import HttpResponse,HttpRequest
from django.contrib import messages


class VaccinatorsList(AbstractAdminListView):
    template_name: str="administrator/vaccinators_list.html"
    queryset= Vacunador.objects.all()

class YellowFeverList(AbstractAdminListView):
    template_name: str="administrator/yellow_fever_list.html"
    queryset= listaDeEsperaFiebreAmarilla.objects.all()


class PatientsList(AbstractAdminListView):
    template_name: str="administrator/patients_list.html"
    queryset= Paciente.objects.all()


class ReasingCovidList(AbstractAdminListView):
    template_name: str="administrator/covid_list.html"
    queryset= listaDeEsperaCovid.objects.all()

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "asignar" in request.POST:
            turno_a_reasignar=listaDeEsperaCovid.objects.get(id=request.POST.get("asignar"))
            turno_a_reasignar.reassign_waitlist()
            messages.success(request,f"Turno reasignado {turno_a_reasignar}")
        return redirect(reverse_lazy("covid_wait_list"))