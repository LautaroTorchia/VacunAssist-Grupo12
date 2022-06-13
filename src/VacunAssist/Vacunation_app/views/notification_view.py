from Vacunation_app.models import Paciente, Turno
from django.shortcuts import render
from django.views.generic.list import ListView
from typing import *
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

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
        turno=Turno.objects.get(id=list(request.POST.keys())[1])
        paciente=Paciente.objects.get(user=request.user)
        self.getnewturn(turno,paciente)
        #Turno.objects.delete(turno)
        return redirect(reverse("notifications"))

    def getnewturn(self,turn,paciente) -> Turno:
        #cambiar para que los de covid sin riesgo los ponga en espere y que los otros se reasignen a partir de la fecha del turno cancelado
        assigner=self.getassigner(paciente)
        if "COVID" in str(turn.vacuna):
            assigner.assign_covid_turn()
        elif "Gripe" in str(turn.vacuna):
            assigner.assign_gripe_turn()

    def getassigner(self,paciente) -> TurnAssigner:
        return TurnAssignerRisk(paciente) if paciente.es_de_riesgo else TurnAssignerNonRisk(paciente)
            