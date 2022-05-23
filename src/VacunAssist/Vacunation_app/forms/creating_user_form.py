from django import forms
from ..models import Usuario


class CreatingUserForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ["email"]

class EnteringDniForm(forms.Form):
    dni=forms.CharField()
    
    
