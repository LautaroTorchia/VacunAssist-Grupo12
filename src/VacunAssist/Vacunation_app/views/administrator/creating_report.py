from datetime import datetime
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
        try:
            fecha_ini=datetime.strptime(request.session["queryset_data"].get("fecha_ini"),'%Y-%m-%d')
            fecha_fin=datetime.strptime(request.session["queryset_data"].get("fecha_fin"),'%Y-%m-%d')
            orden=True if request.session["queryset_data"].get("order")=='Descendente' else False
            order_filter=request.session["queryset_data"].get("order_filter")
            self.queryset=Turno.objects.filter(fecha__gt=fecha_ini,fecha__lt=fecha_fin)

            if order_filter=="DNI":
                self.queryset=sorted(self.queryset,key=lambda x:x.paciente.user.dni,reverse=orden)
            elif order_filter=="Edad":
                self.queryset=sorted(self.queryset,key=lambda x:x.paciente.user.fecha_nac,reverse=orden)
            elif order_filter=="Zona":
                self.queryset=sorted(self.queryset,key=lambda x:x.paciente.user.zona.nombre,reverse=orden)
            elif order_filter=="Vacuna":
                self.queryset=sorted(self.queryset,key=lambda x:x.vacuna.nombre,reverse=orden)
            elif order_filter=="Marca-COVID":
                self.queryset=sorted(self.queryset,key=lambda x:"COVID" in str(x.vacuna),reverse=orden)
            request.session["queryset_data"]={}
        except:
            self.queryset=Turno.objects.none()
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "generate_report" in request.POST:
            form=FiltersSelectorForm(request.POST)
            if form.is_valid():
                fecha_ini=form.cleaned_data.get("fecha_ini")
                fecha_fin=form.cleaned_data.get("fecha_fin")
                order_filter=form.cleaned_data.get("filter")
                orden=form.cleaned_data.get("order")
                request.session["queryset_data"]={"fecha_ini":str(fecha_ini),
                "fecha_fin":str(fecha_fin),"order":orden,"order_filter":order_filter}
            else:
                messages.error(request,"Las fechas estan cruzadas, introduzca fechas validas")
        else:
            pass
            
        
        return redirect(reverse("generate_report"))