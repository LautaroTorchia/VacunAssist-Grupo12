from Vacunation_app.custom_functions import AbstractPacienteListView, create_turn_event
from Vacunation_app.turn_assignment import TurnAssigner, TurnAssignerNonRisk, TurnAssignerRisk
from Vacunation_app.models import Paciente, Turno
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from typing import *



class NotificationView(AbstractPacienteListView):
    template_name: str="notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        paciente=Paciente.objects.get(user=request.user)
        self.queryset=Turno.objects.filter(paciente=paciente).order_by("fecha")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if ("Cancelar","Reasignar") in request.POST:
            try:
                turno=Turno.objects.get(id=request.POST["Cancelar"])
            except:
                turno=Turno.objects.get(id=request.POST["Reasignar"])
            paciente=Paciente.objects.get(user=request.user)
            self.get_new_turn(turno,paciente,request)
            turno.delete()
            return redirect(reverse_lazy("notifications"))

        if "Recordar" in request.POST:
            turno=Turno.objects.get(id=request.POST["Recordar"])
            recordatorio=create_turn_event(turno.fecha,turno.paciente.user.nombre_completo,turno.vacuna,turno.vacunatorio)
            return HttpResponse(recordatorio, content_type='text/calendar')
        return redirect(reverse_lazy("notifications"))

    def get_new_turn(self,turn,paciente,request) -> Turno:
        assigner=self.getassigner(paciente,turn)
        if "COVID" in turn.vacuna.nombre:
            turn = assigner.assign_covid_turn()
            if paciente.es_de_riesgo:
                messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")
            else:
                messages.success(request,f"Como no es de riesgo, queda a la espera de un nuevo turno")
        elif "Gripe" in turn.vacuna.nombre:
            turn = assigner.re_assign_gripe_turn()
            messages.success(request,f"Su turno ha sido reasignado para el {turn.fecha.date()}")
        elif "Fiebre" in turn.vacuna.nombre:
            messages.success(request,"Turno cancelado")
    def getassigner(self,paciente,turn) -> TurnAssigner:
        return TurnAssignerRisk(paciente.user,turn.fecha) if paciente.es_de_riesgo else TurnAssignerNonRisk(paciente.user,turn.fecha)