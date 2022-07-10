from Vacunation_app.forms.update_name_form import NameUpdateForm
from Vacunation_app.models import Vacunatorio
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from typing import Any
from django.http import HttpRequest,HttpResponse


class NameUpdate(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = NameUpdateForm
    template_name = "administrator/vacunatorio_name_update.html"
    permission_required = ("Vacunation_app.Administrador", )
    raise_exception = True

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        instance_form = self.get_form()
        instance_form.is_valid()
        vacunatorio = instance_form.cleaned_data["nombre_actual"]
        nombre_nuevo = instance_form.cleaned_data["nombre_nuevo"]
        try:
            Vacunatorio.objects.get(nombre=nombre_nuevo)
            messages.error(self.request, "Nombre de vacunatorio en uso")
        except Vacunatorio.DoesNotExist:
            vacunatorio.nombre = nombre_nuevo
            vacunatorio.save()
            messages.success(self.request,
                             f"Vacunatorio cambiado a: {vacunatorio.nombre}")
        return redirect(reverse_lazy("change_name"))
