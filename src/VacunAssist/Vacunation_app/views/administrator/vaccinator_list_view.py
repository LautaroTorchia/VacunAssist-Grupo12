from Vacunation_app.custom_classes import PatientPermissionsMixin
from Vacunation_app.models import Usuario
from django.http import HttpResponse,HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from typing import Any

class VaccinatorDelete(PatientPermissionsMixin,TemplateView):
    template_name: str="administrator/vaccinator_delete.html"
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunador = Usuario.objects.get(id=kwargs.get("id"))
        vacunador.delete()
        return redirect(reverse("vaccinators_list"))

