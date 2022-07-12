from typing import Any
from django.http import HttpRequest, HttpResponse
from Vacunation_app.custom_functions import render_to_pdf
from django.views.generic.list import ListView
from Vacunation_app.models import Paciente,  Vacunacion
from Vacunation_app.views.patient.patient_home_view import Usuario


class VaccinationHistoryView(ListView):
    paginate_by: int=5
    template_name: str="patient/vaccination_history.html"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user=Usuario.objects.get(id=kwargs["pk"])
        paciente=Paciente.objects.get(user=user)
        vacunas_covid,vacunas_gripe,vacunas_fiebre=self.create_vaccines_lists(paciente)
        self.extra_context={"covid":vacunas_covid,"gripe":vacunas_gripe,"fiebre":vacunas_fiebre,"nombre_completo":user.nombre_completo}
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user=Usuario.objects.get(id=kwargs["pk"])
        paciente=Paciente.objects.get(user=user)
        vacunas_covid,vacunas_gripe,vacunas_fiebre=self.create_vaccines_lists(paciente)
        pdf=render_to_pdf("pdfs/vaccine_history.html",context_dict={"covid":vacunas_covid,"gripe":vacunas_gripe,"fiebre":vacunas_fiebre})
        return HttpResponse(pdf, content_type='application/pdf')
    
    
    def create_vaccines_lists(self,paciente):
        self.queryset=Vacunacion.objects.filter(paciente=paciente)

        vacunas_covid=self.queryset.filter(vacuna__nombre__contains="COVID")

        vacunas_gripe=list(filter(lambda x:"Gripe" in x.vacuna.nombre,self.queryset))
        vacunas_fiebre=list(filter(lambda x:"Fiebre" in x.vacuna.nombre,self.queryset))
        return vacunas_covid,vacunas_gripe,vacunas_fiebre
