



from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from Vacunation_app.custom_functions import AbstractAdminListView
from Vacunation_app.models import Paciente, Turno
from Vacunation_app.views.patient.patient_home_view import Usuario


class VaccinationHistoryView(AbstractAdminListView):
    template_name: str="patient/vaccination_history.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user=Usuario.objects.get(id=kwargs['pk'])
        paciente=Paciente.objects.get(user=user)
        self.queryset=Turno.objects.filter(paciente=paciente)
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        print("imprime a pdf esto")


        return redirect(reverse("user_home"))