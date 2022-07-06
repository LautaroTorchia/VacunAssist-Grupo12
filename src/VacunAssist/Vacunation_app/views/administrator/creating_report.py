from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from Vacunation_app.custom_functions import AbstractAdminListView
from Vacunation_app.forms.filters import FiltersSelectorForm
from Vacunation_app.models import Turno
from django.contrib import messages


class ReportListView(AbstractAdminListView):
    template_name: str="administrator/reports.html"
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form=FiltersSelectorForm()
        self.extra_context={"form":form}
        if not self.queryset:
            self.queryset= Turno.objects.all()
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "generate_report" in request.POST:
            form=FiltersSelectorForm(request.POST)
            if form.is_valid():
                fecha_ini=form.cleaned_data.get("fecha_ini")
                fecha_fin=form.cleaned_data.get("fecha_fin")
                self.queryset=Turno.objects.filter(fecha__gt=fecha_ini,fecha__lt=fecha_fin)
                print(self.queryset)
            else:
                messages.error(request,"Las fechas estan cruzadas, introduzca fechas validas")
        else:
            pass
            
        
        return redirect(reverse("generate_report"))