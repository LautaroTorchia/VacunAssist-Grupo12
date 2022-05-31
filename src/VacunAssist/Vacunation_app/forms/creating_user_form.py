from django import forms
from ..models import Paciente, Usuario


class CreatingVaccinatorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "zona"]
        error_messages = {
            'email': {
                'unique': ("Registro fallido por email ya registrado")
            }
        }
    

class EnteringDniForm(forms.Form):
    dni = forms.CharField()


class CreatingPatientForm(forms.ModelForm):
    class Meta:
        model= Usuario
        fields=["dni","email",
        "zona","password"]
    ultima_gripe=forms.DateField()
    cantidad_dosis_covid=forms.IntegerField(max_value=2)