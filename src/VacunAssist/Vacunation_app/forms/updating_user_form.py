from django import forms
from ..models import Usuario


#!difiere de la HU en que tiene dos campos de contrasenias
class UpdatingUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'oninvalid':
                "setCustomValidity('Error, la contraseña debe contener más de 6 caracteres')"
            }),
        min_length=6,
        required=False,
        label="Contraseña",
    )

    class Meta:
        model = Usuario
        fields = ["zona"]
