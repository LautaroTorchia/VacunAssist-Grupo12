from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from Vacunation_app.models import Usuario
from django.http import HttpResponse,HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from typing import Any

class VaccinatorDelete(AdministratorPermissionsMixin,TemplateView):
    template_name: str="administrator/vaccinator_delete.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunador = Usuario.objects.get(id=kwargs.get("id"))
        self.extra_context={"vacunador":vacunador}
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunador = Usuario.objects.get(id=kwargs.get("id"))
        vacunador.delete()
        return redirect(reverse("vaccinators_list"))

