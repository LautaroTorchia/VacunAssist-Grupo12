from datetime import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from Vacunation_app.custom_classes import AbstractAdminListView
from Vacunation_app.custom_functions import render_to_pdf
from Vacunation_app.forms.filters import FiltersSelectorForm
from Vacunation_app.models import Turno, Vacunacion
from django.contrib import messages


class ReportListView(AbstractAdminListView):
    template_name: str="administrator/reports.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            form=FiltersSelectorForm(initial=
            {"fecha_ini":request.session["queryset_data"].get("fecha_ini"),
            "fecha_fin":request.session["queryset_data"].get("fecha_fin"),
            "filter":request.session["queryset_data"].get("order_filter"),
            "orden":request.session["queryset_data"].get("order")
            })
        except:
            form=FiltersSelectorForm()
        self.extra_context={"form":form}
        self.get_queries(request)
        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form=FiltersSelectorForm(request.POST)

        if "generate_report" in request.POST:
            if form.is_valid():
                fecha_ini=form.cleaned_data.get("fecha_ini")
                fecha_fin=form.cleaned_data.get("fecha_fin")
                order_filter=form.cleaned_data.get("filter")
                orden=form.cleaned_data.get("order")

                if form.cleaned_data.get("dni_to_filter"):
                    data_to_filter=form.cleaned_data.get("dni_to_filter")
                elif form.cleaned_data.get("vaccine_to_filter"):
                    data_to_filter=form.cleaned_data.get("vaccine_to_filter")
                else:
                    data_to_filter=form.cleaned_data.get("zona_to_filter")

                request.session["queryset_data"]={"fecha_ini":str(fecha_ini),
                "fecha_fin":str(fecha_fin),"order":orden,"order_filter":order_filter,"data_to_filter":str(data_to_filter)}
            else:
                messages.error(request,"Las fechas estan cruzadas, introduzca fechas validas")
        else:
            self.get_queries(request)
            if self.queryset:
                pdf=render_to_pdf("pdfs/report_pdf.html",context_dict={"object_list":self.queryset,"filter":request.session["queryset_data"].get("order_filter")})
                return HttpResponse(pdf, content_type='application/pdf')
            
        return redirect(reverse("generate_report"))

    
    def get_queries(self,request):
        try:
            fecha_ini=datetime.strptime(request.session["queryset_data"].get("fecha_ini"),'%Y-%m-%d')
            fecha_fin=datetime.strptime(request.session["queryset_data"].get("fecha_fin"),'%Y-%m-%d')
            orden=True if request.session["queryset_data"].get("order")=='Descendente' else False
            order_filter=request.session["queryset_data"].get("order_filter")
            data_to_filter=request.session["queryset_data"].get("data_to_filter")
            self.queryset=Vacunacion.objects.filter(fecha__date__gte=fecha_ini,fecha__date__lte=fecha_fin)
            if order_filter=="DNI":
                self.queryset=list(filter(lambda x:str(x.paciente.user.dni).startswith(data_to_filter),self.queryset))
                self.queryset=sorted(self.queryset,key=lambda x:x.paciente.user.dni,reverse=orden)

            elif order_filter=="Zona":
                self.queryset=list(filter(lambda x:str(x.paciente.user.zona.nombre)==data_to_filter,self.queryset))
                self.queryset=sorted(self.queryset,key=lambda x:x.paciente.user.zona.nombre,reverse=orden)

            elif order_filter=="Vacuna":
                self.queryset=list(filter(lambda x:str(x.vacuna.nombre)==data_to_filter,self.queryset))
                self.queryset=sorted(self.queryset,key=lambda x:x.vacuna.nombre,reverse=orden)
            
        except:
            self.queryset=Turno.objects.none()