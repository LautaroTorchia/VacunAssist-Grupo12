from django.views.generic import TemplateView
from Vacunation_app.custom_classes import AdministratorPermissionsMixin


class AdministratorHomeView(AdministratorPermissionsMixin,TemplateView):
    template_name: str="administrator/administrator_view.html"
