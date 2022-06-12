from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.contrib.auth import password_validation
from django.forms import ValidationError

class CustomSetPasswordForm(SetPasswordForm):

    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
    }

    new_password1 = forms.CharField(
        label=("Contraseña nueva"),
        widget=forms.PasswordInput(attrs={"autocomplete": "Contraseña nueva"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Confirme su contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "Confirme su contraseña"}),
    )
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2
