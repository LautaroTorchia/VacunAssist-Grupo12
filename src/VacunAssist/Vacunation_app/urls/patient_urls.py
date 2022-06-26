from Vacunation_app.forms.custom_change_password_form import CustomChangePasswordForm
from Vacunation_app.views.custom_password_change import CustomPasswordChangeView
from Vacunation_app.views.vaccinator_patient_update_view import ProfileUpdate
from Vacunation_app.views.homes.patient_home_view import HomeView
from django.urls import path



urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_user"),
    path('cambiar_contraseña/<int:pk>', CustomPasswordChangeView.as_view(form_class = CustomChangePasswordForm,template_name= "update_password.html" ), name="update_user_password"),
    path("", HomeView.as_view(), name="user_home"),
]