from django import forms
from Vacunation_app.forms.p import PForm
from Vacunation_app.models import Usuario

class UpdatingUserForm(PForm,forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
        required=False,
        label="Contraseña",
    )

    riesgo = forms.BooleanField(
        required=False
    )

    class Meta:
        model = Usuario
        fields = ["zona","profile_pic"]
        labels = {
            "profile_pic": "Foto de perfil",
        }
        error_messages = {
                 'Upload a valid image':"El formato de imagen no es el correcto"
                 }