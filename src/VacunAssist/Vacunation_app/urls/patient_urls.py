from Vacunation_app.views.vaccinator_patient_update_view import ProfileUpdate
from Vacunation_app.views.homes.patient_home_view import HomeView
from django.urls import path


urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_user"),
    path("", HomeView.as_view(), name="user_home"),
]