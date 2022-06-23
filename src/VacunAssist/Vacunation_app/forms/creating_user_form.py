from datetime import date
from django import forms

from Vacunation_app.forms.p import PForm
from ..models import Usuario


class CreatingVaccinatorForm(PForm,forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "zona"]
        error_messages = {
            'email': {
                'unique': ("Registro fallido por email ya registrado")
            }
        }


class EnteringDniForm(PForm,forms.Form):
    dni = forms.CharField()



class CreatingPatientForm(PForm,forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ["dni", "email", "zona", "password"]
        error_messages = {
            'email': {
                'unique': ("Registro fallido por email ya registrado")
            },
            "password": {"min_lenght":("La contraseña debe componerse de 6 carácteres o más")}
        }
        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'DNI'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'zona': forms.Select(attrs={'placeholder': 'Zona'}),
            'password':
            forms.PasswordInput(attrs={'placeholder': 'Contraseña'},render_value=True),
        }
        labels = {
            "dni": "",
            "email": "",
            "password": "",
            "dni": "",
        }
    tiene_gripe=forms.BooleanField(label="Se dio alguna vez la vacuna de la gripe",required=False)
    ultima_gripe = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date',"min":"1990-01-01","max":date.today()}),
        label="Ultima vacuna de gripe",required=False)
    cantidad_dosis_covid = forms.IntegerField(
        max_value=2,
        min_value=0,
        label="",
        widget=forms.NumberInput(
            attrs={'placeholder': 'Cantidad de dosis COVID'}))
    tuvo_amarilla = forms.BooleanField(label="Tiene vacuna de la fiebre amarilla",required=False)
    es_de_riesgo = forms.BooleanField(label="Usted es de riesgo",required=False)
