from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from Vacunation_app.models import Paciente,Turno,listaDeEsperaFiebreAmarilla
from datetime import date
from dateutil.relativedelta import relativedelta

from Vacunation_app.turn_assignment import TurnAssignerRisk
Usuario=get_user_model()


class HomeView(LoginRequiredMixin,TemplateView):
    template_name="patient_homepage.html"
    permission_required = ("Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        paciente= Paciente.objects.get(user=request.user)
        turnos= Turno.objects.filter(paciente=paciente)
        waitlist=listaDeEsperaFiebreAmarilla.objects.filter(paciente=paciente)
        self.extra_context={"turnos": turnos, 
        "puede_fiebre_amarilla": self.puede_fiebre_amarilla(paciente),
        "turno_amarilla": self.turno_amarilla(turnos[0:10]),#Slice por eficiencia
        "esta_en_waitlist": waitlist}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        paciente= Paciente.objects.get(user=request.user)
        if "pedir_turno_amarilla" in request.POST:
            TurnAssignerRisk(patient=paciente).create_amarilla_wait_list_request()
        return redirect(".")
        

    def puede_fiebre_amarilla(self,paciente):
        return paciente.user.fecha_nac.date()+relativedelta(years=60) >= date.today() and not paciente.tuvo_fiebre_amarilla
    def turno_amarilla(self,turnos):
        try:
            return list(filter(lambda turno : "amarilla" in turno.vacuna.nombre and turno.fecha.date() > date.today(),turnos))[0]
        except:
            return None
        

def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
    
def zona_view(request):
    return render(request,"zona.html",{})

def contact_view(request):
    return render(request,"contact.html",{})