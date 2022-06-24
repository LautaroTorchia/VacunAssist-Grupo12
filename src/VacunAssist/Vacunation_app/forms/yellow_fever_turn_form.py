from django import forms
from Vacunation_app.forms.p import PForm
from datetime import date
from datetime import time

class assigningYellowFeverTurn(PForm,forms.Form):
    fecha_del_turno = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date',"min":date.today()}),
        label="Fecha del turno")
    hora_del_turno = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time','min': time(8,0,0) ,'max': time(16,0,0) }))