from Vacunation_app.forms.recover.custom_change_password_form import CustomChangePasswordForm
from Vacunation_app.views.custom_password_change import CustomPasswordChangeView
from Vacunation_app.views.patient.pase_sanitario_view import PaseSanitarioView
from Vacunation_app.views.patient.vaccination_history import VaccinationHistoryView
from Vacunation_app.views.vaccinator_patient_update_view import ProfileUpdate
from Vacunation_app.views.patient.patient_home_view import HomeView
from django.urls import path



urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_user"),
    path('cambiar_contraseña/<int:pk>', CustomPasswordChangeView.as_view(form_class = CustomChangePasswordForm,template_name= "update_password.html" ), name="update_user_password"),
    path("", HomeView.as_view(), name="user_home"),
    path("vaccination_history/<int:pk>", VaccinationHistoryView.as_view(), name="vaccination_history"),
    path("print_pase_sanitario/", PaseSanitarioView.as_view(), name="pase_sanitario"),
]