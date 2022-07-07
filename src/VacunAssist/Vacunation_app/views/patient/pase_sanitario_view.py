from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from Vacunation_app.custom_functions import AbstractAdminListView, render_to_pdf
from Vacunation_app.models import Paciente,Vacunacion
from Vacunation_app.views.patient.patient_home_view import Usuario


class PaseSanitarioView(AbstractAdminListView):
    template_name: str="patient/pase_sanitario.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        paciente=Paciente.objects.get(user=request.user)
        if paciente.dosis_covid==2:
            self.queryset=Vacunacion.objects.filter(paciente=paciente)
            self.queryset=list(filter(lambda x:"COVID" in x.vacuna.nombre,self.queryset))
            
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        paciente=Paciente.objects.get(user=request.user)
        pdf=render_to_pdf("pdfs/pase_sanitario_pdf.html",context_dict={"paciente":paciente})
        print("hice el pdf")
        return HttpResponse(pdf, content_type='application/pdf')

