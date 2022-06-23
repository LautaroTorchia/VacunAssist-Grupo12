from django.urls import path
from Vacunation_app.views.homes.administrator_home_view import *
from Vacunation_app.views.vacunatorio_name_update import NameUpdate
from Vacunation_app.views.stock_view import StockView
from Vacunation_app.views.vaccinator_list_view import *
from Vacunation_app.views.patient_list_view import *
from Vacunation_app.views.yellow_fever_list_view import *
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", administrator_home_view, name="admin_home"),
    path("create_vaccinator/",validating_dni_for_vaccinator_view,name="creating-vaccinator-view"),
    path("create_vaccinator/step2",creating_vaccinator_view,name="create_vaccinator_step2"),
    path("vaccinators_list/", vaccinators_list_view, name="vaccinators_list"),
    path("patients_list/", patients_list_view, name="patients_list"),
    path("stock/", StockView.as_view(), name="stock_view"),
    path('change_name/', NameUpdate.as_view(), name="change_name"),
    path('vaccinator/<int:id>/delete',vaccinator_delete_view,name="vaccinator_delete"),
    path("patients_list/profile/<int:id>",patient_profile_view,name="patient_profile"),
    path("yellow_fever_list/",yellow_fever_list_view,name="yellow_fever_list"),
    path("yellow_fever_list/confirmation/<int:id>",yellow_fever_confirmation_view,name="yellow_fever_confirmation"),
    path("yellow_fever_list/reject/<int:id>",reject_petition_view,name="reject_petition"),
    path('update_administrator',TemplateView.as_view(template_name="administrator_edit_contact.html"),name="admin_contact"),
]