from ..views.vaccinator_patient_update_view import ProfileUpdate
from django.urls import path


urlpatterns = [
    path('editar_perfil/<int:pk>', ProfileUpdate.as_view(), name="update_user"),
]