from django import forms
from ..models import Usuario


class CreatingUserForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ["nombre_completo", "dni", 
        "fecha_nac", "email"]
