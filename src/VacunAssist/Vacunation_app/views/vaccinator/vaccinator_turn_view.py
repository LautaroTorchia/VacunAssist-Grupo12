from datetime import date
from Vacunation_app.models import Paciente, Turno, VacunaEnVacunatorio, Vacunacion, Vacunatorio
from Vacunation_app.turn_assignment import get_new_turn, update_user
from Vacunation_app.custom_functions import render_to_pdf, make_qr
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
from django.views.generic.list import ListView
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse_lazy

class AbstractVaccinatorListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    paginate_by: int= 10
    permission_required: Any= "Vacunation_app.Vacunador"

class TurnsView(AbstractVaccinatorListView):
    template_name: str= "vaccinator/turn_list.html"

    

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunatorio_del_vacunador=Vacunatorio.objects.get(zona=request.user.zona)
        self.queryset= Turno.objects.filter(vacunatorio=vacunatorio_del_vacunador,fecha__day= timezone.now().day).order_by("fecha")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "sin_turno" in request.POST:
            return redirect(reverse_lazy("vaccinator_no_turn"))
        if "falta" in request.POST:
            turno=Turno.objects.get(id=request.POST["falta"])
            get_new_turn(turno)
            messages.success(request,f"Se informo la falta de {turno.paciente}")
        elif "asistencia" in request.POST:
            make_qr()
            turno=Turno.objects.get(id=request.POST["asistencia"])
            pdf=render_to_pdf("pdfs/presence_certificate_pdf.html",{"turno":turno})
            paciente=Paciente.objects.get(user=turno.paciente.user)
            update_user(paciente,turno)
            self.update_stock(turno)
            Vacunacion.objects.create(vacuna=turno.vacuna,vacunatorio=turno.vacunatorio,paciente=turno.paciente,fecha=turno.fecha)
            turno.delete()

            return HttpResponse(pdf, content_type='application/pdf')
        return redirect(reverse_lazy('vaccinator_home'))
    


    def update_stock(self,turno):
        disminucion_de_stock=VacunaEnVacunatorio.objects.get(vacunatorio=turno.vacunatorio,vacuna=turno.vacuna)
        disminucion_de_stock.stock-=1
        disminucion_de_stock.save()