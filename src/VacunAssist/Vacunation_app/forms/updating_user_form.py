from django import forms
from Vacunation_app.models import Usuario

class UpdatingUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
        required=False,
        label="Contraseña",
    )

    class Meta:
        model = Usuario
        fields = ["zona","profile_pic"]