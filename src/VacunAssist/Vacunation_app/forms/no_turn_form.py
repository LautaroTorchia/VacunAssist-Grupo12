from django import forms
from Vacunation_app.forms.p import PForm 
from Vacunation_app.models import Vacunacion

class NoTurnForm(PForm,forms.ModelForm):

    dni = forms.CharField(label='',
            widget=forms.TextInput(attrs={'placeholder': 'DNI'}))

    email = forms.EmailField(
        label=(""),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'placeholder':"Email"}),
    )
    
    class Meta:
        model = Vacunacion
        fields = ["vacuna"]
        labels = {
            "vacuna": "Vacuna",
        }

