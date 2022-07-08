from Vacunation_app.turn_assignment import TurnAssigner, TurnAssignerNonRisk, TurnAssignerRisk
from Vacunation_app.models import Paciente, Turno
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from typing import *


class NotificationView(ListView):
    paginate_by= 10
    template_name: str="notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.has_perm("Vacunation_app.Paciente"):
            paciente=Paciente.objects.get(user=request.user)
            self.queryset=Turno.objects.filter(paciente=paciente).order_by("fecha")
            self.extra_context={"is_staff":False}
            return super().get(request, *args, **kwargs)
        return render(request,self.template_name,{"is_staff":True})

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