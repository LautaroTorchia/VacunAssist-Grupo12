from Vacunation_app.models import Paciente, Turno
from django.shortcuts import render
from django.views.generic.list import ListView
from typing import *
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from Vacunation_app.turn_assignment import TurnAssigner, TurnAssignerNonRisk, TurnAssignerRisk

class NotificationView(ListView):
    paginate_by= 10
    template_name: str="notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.has_perm("Vacunation_app.Paciente"):
            paciente=Paciente.objects.get(user=request.user)
            self.queryset=Turno.objects.filter(paciente=paciente)
        else:
            self.extra_context={"is_staff":"No tenes turnos asignados, ya que eres parte del personal"}
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        print(request.POST)
        #turno=Turno.objects.get(id=list(request.POST.keys())[1])
        #paciente=Paciente.objects.get(user=request.user)
        #self.getnewturn(turno,paciente,request)
        #turno.delete()
        return redirect(".")

    def getnewturn(self,turn,paciente,request) -> Turno:
        assigner=self.getassigner(paciente,turn)
        if "COVID" in str(turn.vacuna):
            turn = assigner.assign_covid_turn()
            if paciente.es_de_riesgo:
                messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")
            else:
                messages.success(request,f"Como no es de riesgo, queda a la espera de un nuevo turno")
        elif "Gripe" in str(turn.vacuna):
            turn = assigner.assign_gripe_turn()
            messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")

    def getassigner(self,paciente,turn) -> TurnAssigner:
        return TurnAssignerRisk(paciente,turn.fecha) if paciente.es_de_riesgo else TurnAssignerNonRisk(paciente,turn.fecha)
            