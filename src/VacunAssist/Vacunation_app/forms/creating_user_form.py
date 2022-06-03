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
        model = Usuario
        fields = ["dni", "email", "zona", "password"]
        error_messages = {
            'email': {
                'unique': ("Registro fallido por email ya registrado")
            }
        }
        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'DNI'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'zona': forms.Select(attrs={'placeholder': 'Zona'}),
            'password':
            forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        }
        labels = {
            "dni": "",
            "email": "",
            "password": "",
            "dni": "",
        }

    ultima_gripe = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Ultima vacuna de gripe")
    cantidad_dosis_covid = forms.IntegerField(
        max_value=2,
        min_value=0,
        label="",
        widget=forms.NumberInput(
            attrs={'placeholder': 'Cantidad de dosis COVID'}))
    tuvo_amarilla = forms.BooleanField(label="Tiene vacuna de fiebre amarilla")
