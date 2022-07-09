from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse,HttpRequest
from django.views.generic.list import ListView
from typing import Any

class AdministratorPermissionsMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required: Any= "Vacunation_app.Administrador"

class VaccinatorPermissionsMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required: Any= "Vacunation_app.Vacunador"

class PatientPermissionsMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required: Any= "Vacunation_app.Vacunador"

class AbstractAdminListView(AdministratorPermissionsMixin,ListView):
    paginate_by: int= 5

class AbstractVaccinatorListView(VaccinatorPermissionsMixin,ListView):
    paginate_by: int= 5

class AbstractPatientListView(PatientPermissionsMixin,ListView):
    paginate_by: int= 5



