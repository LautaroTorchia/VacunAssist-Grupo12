from Vacunation_app.views.homes.vaccinator_home_view import HomeView
from Vacunation_app.views.vaccinator_patient_update_view import ProfileUpdate
from django.urls import path

urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_vaccinator"),
    path("", HomeView.as_view(), name="vaccinator_home"),
]