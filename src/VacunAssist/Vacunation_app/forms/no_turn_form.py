from django import forms
from Vacunation_app.forms.p import PForm 
from Vacunation_app.models import Vacunacion

class NoTurnForm(PForm,forms.ModelForm):

    dni = forms.CharField(label='',
            widget=forms.TextInput(attrs={'placeholder': 'DNI'}))

    class Meta:
        model = Vacunacion
        fields = ["vacuna"]
        labels = {
            "vacuna": "Vacuna",
        }

