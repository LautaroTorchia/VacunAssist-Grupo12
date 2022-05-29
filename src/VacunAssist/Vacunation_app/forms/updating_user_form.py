from distutils.command.clean import clean
from django import forms
from ..models import Usuario


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