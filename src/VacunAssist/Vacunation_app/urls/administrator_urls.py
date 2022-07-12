from django.urls import path
from Vacunation_app.views.administrator.creating_report import ReportListView
from Vacunation_app.views.administrator.vacunatorio_name_update import NameUpdate
from Vacunation_app.views.administrator.stock_view import StockView
from Vacunation_app.views.administrator.vaccinator_list_view import VaccinatorDelete
from Vacunation_app.views.administrator.administrator_home_view import AdministratorHomeView
from Vacunation_app.views.administrator.patient_profile_view import AdminViewProfile
from Vacunation_app.views.administrator.create_vaccinator import CreateVaccinatorDNI, ValidateVaccinatorDNI
from Vacunation_app.views.administrator.yellow_fever_management_view import RejectYellowFever, ConfirmYellowFever
from Vacunation_app.views.administrator.administrator_lists import VaccinatorsList,PatientsList,YellowFeverList,ReassingCovidList
from Vacunation_app.views.administrator.statistics import StatsView
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", AdministratorHomeView.as_view(), name="admin_home"),
    path("create_vaccinator/", ValidateVaccinatorDNI.as_view(),name="creating_vaccinator_view"),
    path("create_vaccinator/step2", CreateVaccinatorDNI.as_view(),name="create_vaccinator_step2"),
    path("vaccinators_list/", VaccinatorsList.as_view(), name="vaccinators_list"),
    path("patients_list/", PatientsList.as_view(), name="patients_list"),
    path("stock/", StockView.as_view(), name="stock_view"),
    path('change_name/', NameUpdate.as_view(), name="change_name"),
    path('vaccinator/<int:id>/delete',VaccinatorDelete.as_view(),name="vaccinator_delete"),
    path("patients_list/profile/<int:pk>",AdminViewProfile.as_view(),name="patient_profile"),
    path("yellow_fever_list/reject/<int:id>",RejectYellowFever.as_view(),name="reject_petition"),
    path("yellow_fever_list/", YellowFeverList.as_view(),name="yellow_fever_list"),
    path("covid_wait_list/", ReassingCovidList.as_view(),name="covid_wait_list"),
    path("yellow_fever_list/confirmation/<int:id>",ConfirmYellowFever.as_view(),name="yellow_fever_confirmation"),
    path('update_administrator',TemplateView.as_view(template_name="administrator/administrator_edit_contact.html"),name="admin_contact"),
    path('generate_report',ReportListView.as_view(),name="generate_report"),
    path('statistics/',StatsView.as_view(),name="statistics"),
]