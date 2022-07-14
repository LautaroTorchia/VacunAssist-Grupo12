from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from django.views.generic import TemplateView
from typing import Any
from django.http import HttpRequest,HttpResponse
from Vacunation_app.custom_functions import calculate_age
from Vacunation_app.models import AbstractVacunation, Paciente, Turno, Vacuna, Vacunatorio
import plotly.express as px
import pandas as pd
from django.shortcuts import render
import plotly.graph_objects as go



class StatsView(AdministratorPermissionsMixin,TemplateView):
    template_name: str="administrator/statistics.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        #series = df.groupby(["vacuna__nombre"])["vacuna__nombre"].count()

        self.extra_context={"chart":self.proporcion_vacunaciones_chart(),"chart2":self.pacientes_por_zona()
            ,"chart3":self.pacientes_por_grupo_etario(),"chart4":self.vacunas_pendientes_por_vacunatorio()}
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
        fig=px.bar(df, title='Cantidad de pacientes por zona',
        labels={
                     "value": "",
                     "index": f"Zona con más pacientes: {series.idxmax()}"
                 })
        fig.update_layout(yaxis={"dtick":1})
        return fig.to_html()

    def pacientes_por_grupo_etario(self):
        fechas=Paciente.objects.values_list("user__fecha_nac",flat=True)
        edades=list(map(lambda f: calculate_age(f),fechas))
        grupos=pd.DataFrame(edades,columns=["Edad"])
        bins= [0,18,60,1000]
        labels = ['Menor de 18','Entre 18 y 60','60 o más']
        grupos['GrupoEtario'] = pd.cut(grupos['Edad'], bins=bins, labels=labels, right=False)
        grupos=grupos.groupby("GrupoEtario").count()
        fig = go.Figure(go.Indicator(value = sum(edades)/len(edades),title = {"text": "Edad promedio de los pacientes"}))
        fig.add_trace(go.Bar(
            y=grupos["Edad"],x=grupos.unstack()["Edad"].index))
        fig.update_layout(yaxis={"dtick":1},title="Cantidad de pacientes por grupo etario")
        return fig.to_html()

    def vacunas_pendientes_por_vacunatorio(self):
        turnos=pd.DataFrame(Turno.objects.all().values())[["vacuna_id","vacunatorio_id"]]
        vacunatorios=pd.DataFrame(Vacunatorio.objects.values())[["id","nombre"]]
        vacunas=pd.DataFrame(Vacuna.objects.values())[["id","nombre"]]
        turnos.vacunatorio_id.replace(list(vacunatorios["id"]),list(vacunatorios["nombre"]),inplace=True)
        turnos.vacuna_id.replace(list(vacunas["id"]),list(vacunas["nombre"]),inplace=True)
        turnos.insert(0, 'Num', 1)
        fig = px.bar(turnos, x='vacunatorio_id', y='Num',color='vacuna_id',labels={
                     "Num": "",
                     "vacunatorio_id": "Vacunatorio",
                     "vacuna_id":"Vacuna"
                 })
        fig.update_layout(yaxis={"dtick":1},title="Vacunas que se necesitaran en el futuro")


        return fig.to_html()
