from django.views.generic.list import ListView
from Vacunation_app.models import Turno, Vacunador
from django.http import HttpRequest,HttpResponse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class TurnView(ListView,LoginRequiredMixin,PermissionRequiredMixin):
    paginate_by= 10
    template_name: str="notifications_vaccinator.html"
    permission_required: Any= "Vacunation_app.Vacunador"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunador=Vacunador.objects.get(user=request.user)
        self.queryset=Turno.objects.filter(vacunador=vacunador,vacunatorio=vacunador.vacunatorio)
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        turno=Turno.objects.get(id=list(request.POST.keys())[1])
        if "Informar" in request.POST:
            print("Aca se informa que no asistió")
        elif "Confirmar" in request.POST:
            print("Aca se genera el pdf con el certificado de asistencia")

        return redirect(reverse("notifications"))