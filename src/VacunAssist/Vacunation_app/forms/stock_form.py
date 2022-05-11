from django import forms
from Vacunation_app.models import VacunaEnVacunatorio
from ..constants import *

class StockForm (forms.ModelForm):

    class Meta:
        model = VacunaEnVacunatorio
        fields = ["vacunatorio", "vacuna", 
        "stock"]