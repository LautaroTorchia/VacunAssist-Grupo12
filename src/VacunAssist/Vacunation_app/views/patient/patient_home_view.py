from Vacunation_app.custom_classes import PatientPermissionsMixin
from Vacunation_app.models import Paciente,Turno, listaDeEsperaCovid,listaDeEsperaFiebreAmarilla
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.views.generic.base import TemplateView
from django.http.response import HttpResponseBase
from django.shortcuts import redirect, render
from django.utils import timezone
from django.http import HttpRequest
from dateutil.relativedelta import relativedelta
from typing import Any


from Vacunation_app.turn_assignment import TurnAssignerRisk
Usuario=get_user_model()


class HomeView(PatientPermissionsMixin,TemplateView):
    template_name="patient/patient_homepage.html"

    def get(self, request, *args, **kwargs):
        paciente= Paciente.objects.get(user=request.user)
        turnos= Turno.objects.filter(paciente=paciente,fecha__gt=timezone.now().date())
        waitlist_fiebre=listaDeEsperaFiebreAmarilla.objects.filter(paciente=paciente)
        waitlist_covid=listaDeEsperaCovid.objects.filter(paciente=paciente)
        self.extra_context={"turnos": turnos, 
        "puede_fiebre_amarilla": self.puede_fiebre_amarilla(paciente),
        "turno_amarilla": self.turno_vacuna(turnos[0:10],"amarilla"),
        "esta_en_waitlist": waitlist_fiebre,
        "turno_gripe": self.turno_vacuna(turnos[0:10],"Gripe"),
        "turno_covid": self.turno_vacuna(turnos[0:10],"COVID"),
        "waitlist_covid":waitlist_covid,
        "turns":turnos
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "pedir_turno_amarilla" in request.POST:
            TurnAssignerRisk(request.user).create_amarilla_wait_list_request()
        return redirect(".")
        
    def puede_fiebre_amarilla(self,paciente):
        return paciente.user.fecha_nac.date()+relativedelta(years=60) >= timezone.now().date() and not paciente.tuvo_fiebre_amarilla

    def turno_vacuna(self,turnos,name):
        try:
            return list(filter(lambda turno : name in turno.vacuna.nombre and turno.fecha.date() >= timezone.now().date(),turnos))[0]
        except:
            return None
        

class LogOut(LoginRequiredMixin,RedirectView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        logout(request)
        self.pattern_name="login"
        return super().get(request, *args, **kwargs)

class Zona(LoginRequiredMixin,TemplateView):
    template_name: str="zona.html"

class Contact(LoginRequiredMixin,TemplateView):
    template_name: str="contact.html"