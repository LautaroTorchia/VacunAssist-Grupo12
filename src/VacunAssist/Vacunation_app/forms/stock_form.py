from django import forms
from Vacunation_app.models import VacunaEnVacunatorio
from ..constants import *
from Vacunation_app.forms.p import PForm

class StockForm (PForm,forms.ModelForm):
    class Meta:
        model = VacunaEnVacunatorio
        fields = ["vacunatorio", "vacuna", "stock"]