from django import forms
from ..models import Usuario


class CreatingUserForm(forms.ModelForm):
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
