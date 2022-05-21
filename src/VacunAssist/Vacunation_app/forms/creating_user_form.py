from django import forms
from ..models import Usuario


class CreatingUserForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ["nombre_completo",
        "fecha_nac", "email"]

class EnteringDniForm(forms.Form):
    dni=forms.CharField()
    
    
