from Vacunation_app.forms.custom_set_password_form import CustomSetPasswordForm
from django.forms import ValidationError
from django import forms


class CustomChangePasswordForm(CustomSetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    error_messages = {
        **CustomSetPasswordForm.error_messages,
        "password_incorrect": (
            "Tu contraseña actual no es la correcta. Por favor intenta de nuevo"
        ),
    }
    old_password = forms.CharField(
        label= (""),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,"placeholder":"Contraseña actual"}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password