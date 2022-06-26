from django.contrib.auth.forms import SetPasswordForm
from Vacunation_app.forms.p import PForm
from django import forms
from django.contrib.auth import password_validation
from django.forms import ValidationError

class CustomSetPasswordForm(PForm,SetPasswordForm):

    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
    }

    new_password1 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={"autocomplete": "Contraseña nueva","placeholder":"Contraseña nueva"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "Confirme su contraseña","placeholder":"Confirme su contraseña"}),
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

