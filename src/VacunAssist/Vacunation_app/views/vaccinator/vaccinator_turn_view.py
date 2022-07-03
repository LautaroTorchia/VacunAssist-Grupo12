from django.views.generic.list import ListView
from typing import Any
from django.http import HttpRequest,HttpResponse
from Vacunation_app.models import Turno, Vacunatorio
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        turno=Turno.objects.get(id=request.POST["Informar falta"])
        if "Informar falta" in request.POST:
            print("Aca se informa que no asistió")
        elif "Confirmar asistencia" in request.POST:
            print("Aca se genera el pdf con el certificado de asistencia")

        return redirect(reverse("notifications"))