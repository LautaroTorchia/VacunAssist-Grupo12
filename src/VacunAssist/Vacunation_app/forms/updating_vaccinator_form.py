from django import forms
from Vacunation_app.forms.p import PForm
from Vacunation_app.models import Usuario

class UpdatingVaccinatorForm(PForm,forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["zona","profile_pic"]
        labels = {
            "profile_pic": "Foto de perfil",
        }
        error_messages = {
                 'Upload a valid image':"El formato de imagen no es el correcto"
                 }

