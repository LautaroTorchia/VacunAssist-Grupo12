from datetime import date
from Vacunation_app.models import Paciente, Turno, VacunaEnVacunatorio, Vacunacion, Vacunatorio
from Vacunation_app.turn_assignment import getnewturn
from Vacunation_app.custom_functions import render_to_pdf, make_qr
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.contrib.staticfiles.finders import find as find_static_file
from django.utils import timezone
from django.views.generic.list import ListView
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
        if "falta" in request.POST:
            turno=Turno.objects.get(id=request.POST["falta"])
            getnewturn(turno)
            messages.success(request,f"Se informo la falta de {turno.paciente}")
        elif "asistencia" in request.POST:
            make_qr()
            turno=Turno.objects.get(id=request.POST["asistencia"])
            pdf=render_to_pdf("pdfs/presence_certificate_pdf.html",{"turno":turno,"background":find_static_file("qr/qr.png")})
            paciente=Paciente.objects.get(user=turno.paciente.user)
            self.update_user(paciente,turno)
            self.update_stock(turno)
            Vacunacion.objects.create(vacuna=turno.vacuna,vacunatorio=turno.vacunatorio,paciente=turno.paciente,fecha=turno.fecha)
            turno.delete()

        return HttpResponse(pdf, content_type='application/pdf')
    
    def update_user(paciente,turno):
        if "gripe" in turno.vacuna.nombre:
            paciente.fecha_gripe=date.today()
        elif "COVID" in turno.vacuna.nombre:
            paciente.dosis_covid+=1
        else:
            paciente.tuvo_fiebre_amarilla=True
        paciente.save()

    def update_stock(turno):
        disminucion_de_stock=VacunaEnVacunatorio.objects.get(vacunatorio=turno.vacunatorio,vacuna=turno.vacuna)
        disminucion_de_stock-=1
        disminucion_de_stock.save()
