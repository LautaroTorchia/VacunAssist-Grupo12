from django import forms
from ..models import Usuario


#!difiere de la HU en que tiene dos campos de contrasenias
class UpdatingUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["password"]
        widget = {
            "password":
            forms.CharField(
                min_length=1,
                label="",
                widget=forms.TextInput(attrs={'placeholder': 'Contraseña'}))
        }
