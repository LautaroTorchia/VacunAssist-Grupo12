from django.urls import path
from Vacunation_app.views.homes.administrator_home_view import *
from Vacunation_app.views.vacunatorio_name_update import NameUpdate
from Vacunation_app.views.stock_view import StockView
from Vacunation_app.views.vaccinator_list_view import *
from django.views.generic.base import TemplateView


urlpatterns = [
    path("", administrator_home_view, name="admin_home"),
    path("create_vaccinator/",validating_dni_for_vaccinator_view, name="creating-vaccinator-view"),
    path("create_vaccinator/step2",creating_vaccinator_view, name="create_vaccinator_step2"),
    path("vaccinators_list/", vaccinators_list_view, name="vaccinators_list"),
    path("stock/", StockView.as_view(), name="stock_view"),
    path('change_name/', NameUpdate.as_view(), name="change_name"),
    path('vaccinator/<int:id>/delete', vaccinator_delete_view, name="vaccinator_delete"),
    path('update_administrator', TemplateView.as_view(template_name = "administrator_edit_contact.html"), name="admin_contact"),
]