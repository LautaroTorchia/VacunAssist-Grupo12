from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from django.views.generic import TemplateView
from typing import Any
from django.http import HttpRequest,HttpResponse
from Vacunation_app.custom_functions import calculate_age
from Vacunation_app.models import AbstractVacunation, Paciente
import plotly.express as px
import pandas as pd
from django.shortcuts import render
import plotly.graph_objects as go



class StatsView(AdministratorPermissionsMixin,TemplateView):
    template_name: str="administrator/statistics.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        #series = df.groupby(["vacuna__nombre"])["vacuna__nombre"].count()

        self.extra_context={"chart":self.proporcion_vacunaciones_chart(),"chart2":self.pacientes_por_zona(),"chart3":self.pacientes_por_edad()}
        return render(request,self.template_name,self.extra_context)
        
    def proporcion_vacunaciones_chart(self):
        nombres=AbstractVacunation.objects.values("vacuna__nombre")
        df = pd.DataFrame(list(nombres))
        fig=px.pie(df, names='vacuna__nombre', title='Proporcion de vacunas dadas')
        return fig.to_html()

    def pacientes_por_zona(self):
        nombres=Paciente.objects.values_list("user__zona__nombre", flat=True)
        df = pd.DataFrame(nombres,columns=["Cantidad"])
        series = df.groupby(["Cantidad"])["Cantidad"].count()
        df=pd.DataFrame(series)
        fig=px.bar(df, title='Pacientes por zona')
        return fig.to_html()

    def pacientes_por_edad(self):
        fechas=Paciente.objects.values_list("user__fecha_nac",flat=True)
        fechas=list(map(lambda f: calculate_age(f),fechas))

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            value = sum(fechas)/len(fechas),
            gauge = {
                'axis': {'visible': False}},
            domain = {'row': 0, 'column': 0}))

        fig.update_layout(
            grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
            template = {'data' : {'indicator': [{
                'title': {'text': "Edad promedio"},
                'mode' : "number+delta+gauge"}]
                                }})

        return fig.to_html()

