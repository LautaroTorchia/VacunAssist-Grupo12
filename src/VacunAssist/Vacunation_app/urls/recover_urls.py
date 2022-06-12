from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views
from Vacunation_app.forms.custom_set_password_form import CustomSetPasswordForm
from Vacunation_app.forms.ClaveResetForm import ClaveResetForm

urlpatterns = [
    path("password_reset/", auth_views.PasswordResetView.as_view(
    template_name= "registration/password_reset_view.html"
    ,email_template_name= "emails/password_reset_email.html"
    ,subject_template_name = "emails/password_reset_subject.txt"
    ), name="password_reset"),

    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(
    template_name= "registration/password_reset_done_view.html"
    ),name="password_reset_done",),
    
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(
    template_name= "registration/password_reset_confirm_view.html",
    form_class = CustomSetPasswordForm
    ),name="password_reset_confirm",),#Arreglar los errores que están arriba

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name= "registration/password_reset_complete_view.html"
    ),name="password_reset_complete",),
    
    path("clave_reset/", auth_views.PasswordResetView.as_view(
    template_name= "registration/clave_reset_view.html",
    form_class=ClaveResetForm,
    subject_template_name="emails/clave_reset_subject.txt",
    email_template_name="emails/clave_reset_email.html",
    success_url=reverse_lazy("clave_reset_done")
    ),name="clave_reset",),

    path("clave_reset/done/", auth_views.PasswordResetDoneView.as_view(
    template_name= "registration/clave_reset_done_view.html"),name="clave_reset_done",),
]