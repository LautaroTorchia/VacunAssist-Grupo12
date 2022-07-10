from Vacunation_app.custom_classes import AbstractVaccinatorListView
from Vacunation_app.models import Turno, Vacunatorio
from Vacunation_app.custom_functions import render_to_pdf, make_qr, vacunassist_send_mail
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse




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
            turno.reassign_turn()
            messages.success(request,f"Se informo la falta de {turno.paciente}")
        elif "asistencia" in request.POST:
            turno=Turno.objects.get(id=request.POST["asistencia"])
            make_qr(request.build_absolute_uri().split("vaccinator/")[0]+reverse('vaccination_history',args=[turno.paciente.user.id]))
            turno=Turno.objects.get(id=request.POST["asistencia"])
            pdf=render_to_pdf("pdfs/presence_certificate_pdf.html",{"turno":turno})
            vacunacion=turno.vacunar_de_turno()
            messages.success(request,f"Se guardo la vacunación de {turno.paciente}")
            vacunassist_send_mail(
                "emails/registered_vacunated_email.html",{"vacunacion":vacunacion,"paciente":turno.paciente}
                ,"Vacunación en Vacunassist",turno.paciente.user.email,pdf)

        return redirect(reverse_lazy('vaccinator_home'))
    


