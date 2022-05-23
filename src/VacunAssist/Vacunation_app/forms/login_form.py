from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm (AuthenticationForm):
    dni_o_mail = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput())
    username=None
    password=None
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )


class LoginClaveForm (AuthenticationForm):
    clave = forms.CharField(max_length=4, label='',
            widget=forms.TextInput(attrs={'placeholder': 'Clave'}))
    username=None
    password=None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )