
from Vacunation_app.models import VacunaEnVacunatorio, Vacunatorio
from Vacunation_app.forms.stock_form import StockForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView
from typing import Any
from django.http import HttpRequest,HttpResponse,HttpResponseNotModified
from django.urls import reverse_lazy
from django.shortcuts import redirect


class StockView(FormView,LoginRequiredMixin,PermissionRequiredMixin):
    template_name: str="administrator/stock_view.html"
    form_class= StockForm
    permission_required="Vacunation_app.Administrador"
    success_url= reverse_lazy("stock_view")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vaccine_info = VacunaEnVacunatorio.objects.all()
        vaccination_center_info = Vacunatorio.objects.all()
        self.extra_context= {"vaccine_info": vaccine_info,"vaccination_center_info": vaccination_center_info}
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        stock_form=self.get_form()
        if stock_form.is_valid():
            vacuna = stock_form.cleaned_data.get("vacuna")
            vacunatorio = stock_form.cleaned_data.get("vacunatorio")
            vacunation_to_update = VacunaEnVacunatorio.objects.get(vacuna=vacuna, vacunatorio=vacunatorio)

            if "aumentar" in request.POST:
                vacunation_to_update.stock += stock_form.cleaned_data.get("stock")
                messages.success(request,"Stock aumentado")
                vacunation_to_update.save()
            elif "disminuir" in request.POST:
                if vacunation_to_update.stock < stock_form.cleaned_data.get("stock"):
                    messages.error(request,"No hay stock suficiente")
                else:
                    vacunation_to_update.stock -= stock_form.cleaned_data.get("stock")
                    messages.success(request,"Stock disminuido")
                    vacunation_to_update.save()
        return redirect(self.success_url)
    


