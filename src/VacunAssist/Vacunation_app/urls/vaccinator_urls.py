from Vacunation_app.forms.recover.custom_change_password_form import CustomChangePasswordForm
from Vacunation_app.views.custom_password_change import CustomPasswordChangeView
from Vacunation_app.views.vaccinator.vaccinator_turn_view import TurnsView
from Vacunation_app.views.vaccinator.vaccinator_no_turn_register import NoTurnView
from Vacunation_app.views.vaccinator_patient_update_view import ProfileUpdate
from django.urls import path


urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_vaccinator"),
    path('cambiar_contraseña/<int:pk>', CustomPasswordChangeView.as_view(form_class = CustomChangePasswordForm,template_name= "update_password.html" ), name="update_vaccinator_password"),
    path('', TurnsView.as_view(), name='vaccinator_home'),
    path('sin_turno', NoTurnView.as_view(), name='vaccinator_no_turn'),
]