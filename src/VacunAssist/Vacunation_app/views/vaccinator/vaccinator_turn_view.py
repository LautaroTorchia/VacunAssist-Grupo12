from Vacunation_app.models import Turno, Vacunatorio
from Vacunation_app.turn_assignment import getnewturn
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy
from typing import Any

class AbstractVaccinatorListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    paginate_by: int= 10
    permission_required: Any= "Vacunation_app.Vacunador"

class TurnsView(AbstractVaccinatorListView):
    template_name: str= "vaccinator/turn_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunatorio_del_vacunador=Vacunatorio.objects.get(zona=request.user.zona)
        self.queryset= Turno.objects.filter(vacunatorio=vacunatorio_del_vacunador).filter(fecha__day= timezone.now().day)
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        print(request.POST)
        if "falta" in request.POST:
            turno=Turno.objects.get(id=request.POST["falta"])
            getnewturn(turno)
            messages.success(request,f"Se informo la falta de {turno.paciente}")
        elif "asistencia" in request.POST:
            turno=Turno.objects.get(id=request.POST["asistencia"])
            print("Aca se genera el pdf con el certificado de asistencia")
        return redirect(reverse_lazy("vaccinator_turns"))