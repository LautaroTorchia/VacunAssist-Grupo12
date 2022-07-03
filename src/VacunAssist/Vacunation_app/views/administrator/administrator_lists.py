from Vacunation_app.models import Vacunador, Paciente, listaDeEsperaFiebreAmarilla
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from typing import Any
from django.http import HttpResponse,HttpRequest

class AbstractAdminListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    paginate_by= 10
    permission_required: Any= "Vacunation_app.Administrador"

class VaccinatorsList(AbstractAdminListView):
    template_name: str="administrator/vaccinators_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= Vacunador.objects.all()
        return super().get(request, *args, **kwargs)

class YellowFeverList(AbstractAdminListView):
    template_name: str="administrator/yellow_fever_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= listaDeEsperaFiebreAmarilla.objects.all()
        return super().get(request, *args, **kwargs)

class PatientsList(AbstractAdminListView):
    template_name: str="administrator/patients_list.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset= Paciente.objects.all()
        return super().get(request, *args, **kwargs)
