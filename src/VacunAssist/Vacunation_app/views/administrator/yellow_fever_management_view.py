from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from Vacunation_app.custom_functions import vacunassist_send_mail
from Vacunation_app.forms.yellow_fever_turn_form import assigningYellowFeverTurn
from Vacunation_app.models import listaDeEsperaFiebreAmarilla, Turno
from Vacunation_app.turn_assignment import TurnAssignerYellowFever
from django.urls import reverse
from django.views.generic import RedirectView,FormView
from django.http.response import HttpResponseBase
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from typing import Any
from datetime import datetime

class ConfirmYellowFever(AdministratorPermissionsMixin,FormView):
    template_name="administrator/yellow_fever_confirmation.html"
    form_class=assigningYellowFeverTurn

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        petition = listaDeEsperaFiebreAmarilla.objects.get(id=kwargs.get("id"))
        self.extra_context={"petition":petition}
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        petition = listaDeEsperaFiebreAmarilla.objects.get(id=kwargs.get("id"))
        form=self.get_form()
        form.is_valid()
        fecha=datetime.combine(form.cleaned_data["fecha_del_turno"],form.cleaned_data["hora_del_turno"])
        if Turno.objects.filter(fecha=fecha).exists:
            messages.error(request,"Esa fecha y hora ya tiene un turno registrado, asigne otra fecha")
            self.success_url= reverse("yellow_fever_confirmation",args=[kwargs.get("id")])
        else:
            TurnAssignerYellowFever(petition.paciente).assign_yellow_fever_turn(fecha,petition.vacunatorio)
            vacunassist_send_mail('emails/rechazo_fiebre.html',{"fecha":fecha},"Tu solicitud de turno de fiebre amarilla fue aceptada",petition.paciente.user.email)
            petition.delete()
            messages.success(request,f"Turno asignado con exito en {fecha}")
            self.success_url= reverse("yellow_fever_list")
        return super().post(request, *args, **kwargs)

class RejectYellowFever(AdministratorPermissionsMixin,RedirectView):
    pattern_name="yellow_fever_list"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        petition = listaDeEsperaFiebreAmarilla.objects.get(id=kwargs.get("id"))
        vacunassist_send_mail('emails/rechazo_fiebre.html',{},"Tu solicitud de turno de fiebre amarilla fue rechazada",petition.paciente.user.email)
        petition.delete()
        messages.success(request,"Turno rechazado")
        kwargs={}
        return super().get(request, *args, **kwargs)
    