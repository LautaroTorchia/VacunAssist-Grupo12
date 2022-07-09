from Vacunation_app.turn_assignment import TurnAssigner, TurnAssignerNonRisk, TurnAssignerRisk
from Vacunation_app.models import Paciente, Turno
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from typing import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AbstractPacienteListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    paginate_by= 10
    permission_required: Any="Vacunation_app.Paciente"
    raise_exception: bool=True

class NotificationView(AbstractPacienteListView):
    template_name: str="notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        paciente=Paciente.objects.get(user=request.user)
        self.queryset=Turno.objects.filter(paciente=paciente).order_by("fecha")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        turno=Turno.objects.get(id=list(request.POST.keys())[1])
        paciente=Paciente.objects.get(user=request.user)
        self.get_new_turn(turno,paciente,request)
        turno.delete()

        return redirect(reverse_lazy("notifications"))

    def get_new_turn(self,turn,paciente,request) -> Turno:
        assigner=self.getassigner(paciente,turn)
        if "COVID" in str(turn.vacuna):
            turn = assigner.assign_covid_turn()
            if paciente.es_de_riesgo:
                messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")
            else:
                messages.success(request,f"Como no es de riesgo, queda a la espera de un nuevo turno")
        elif "Gripe" in str(turn.vacuna):
            turn = assigner.re_assign_gripe_turn()
            messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")
        elif "Fiebre" in str(turn.vacuna):
            messages.success(request,"Turno cancelado")
    def getassigner(self,paciente,turn) -> TurnAssigner:
        return TurnAssignerRisk(paciente.user,turn.fecha) if paciente.es_de_riesgo else TurnAssignerNonRisk(paciente.user,turn.fecha)