from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from Vacunation_app.models import Paciente
from django.views.generic import DetailView

class AdminViewProfile(AdministratorPermissionsMixin,DetailView):
    template_name: str="administrator/patient_profile.html"
    model= Paciente