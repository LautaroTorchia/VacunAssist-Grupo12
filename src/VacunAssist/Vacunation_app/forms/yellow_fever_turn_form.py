from django import forms
from Vacunation_app.forms.p import PForm
from datetime import date
import datetime

class assigningYellowFeverTurn(PForm,forms.Form):
    fecha_del_turno = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date',"min":date.today()}),
        label="Fecha del turno")
    hora_del_turno = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time','min': datetime.datetime.now().replace(hour=8,minute=0) }))