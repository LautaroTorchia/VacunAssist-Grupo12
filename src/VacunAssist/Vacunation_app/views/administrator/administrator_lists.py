from django.shortcuts import redirect
from django.urls import  reverse_lazy
from Vacunation_app.custom_functions import AbstractAdminListView
from Vacunation_app.models import Vacunador, Paciente, listaDeEsperaFiebreAmarilla, listaDeEsperaCovid
from typing import Any
from django.http import HttpResponse,HttpRequest
from django.contrib import messages


class VaccinatorsList(AbstractAdminListView):
    template_name: str="administrator/vaccinators_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= Vacunador.objects.all()
        return super().get(request, *args, **kwargs)

class YellowFeverList(AbstractAdminListView):
    template_name: str="administrator/yellow_fever_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= listaDeEsperaFiebreAmarilla.objects.all()
        return super().get(request, *args, **kwargs)

class PatientsList(AbstractAdminListView):
    template_name: str="administrator/patients_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= Paciente.objects.all()
        return super().get(request, *args, **kwargs)

class ReasingCovidList(AbstractAdminListView):
    template_name: str="administrator/covid_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= listaDeEsperaCovid.objects.all()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "reasignar" in request.POST:
            turno_a_reasignar=listaDeEsperaCovid.objects.get(id=request.POST.get("reasignar"))
            turno_a_reasignar.reassign_waitlist()
            messages.success(request,f"Turno reasignado {turno_a_reasignar}")
        return redirect(reverse_lazy("covid_wait_list"))