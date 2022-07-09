from django import forms
from Vacunation_app.forms.p import PForm
from django.utils import timezone
from datetime import time

class assigningYellowFeverTurn(PForm,forms.Form):
    fecha_del_turno = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date',"min":timezone.now().date()}),
        label="Fecha del turno")
    hora_del_turno = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time','min': time(8,0,0) ,'max': time(16,0,0) }))