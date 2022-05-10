from django import forms
from models import Usuario
class LoginForm (forms.Form):
    dni_o_mail = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

#    def clean_dni_o_mail(self,*args,**kwargs):
#        dnilogin=self.cleaned_data.get("dni")
#        usu = Usuario.objects.get(dni = dnilogin)
#        if not usu:
#            maillogin=self.cleaned_data.get("email")
#            usu = Usuario.objects.get(email = maillogin)
#            if not usu:
#                raise forms.ValidationError("Usuario inexistente")
#            return maillogin
#        return dnilogin

class LoginClaveForm (forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginClaveForm, self).__init__(*args, **kwargs)
    clave = forms.CharField(max_length=4)
#    def clean_clave(self,*args,**kwargs):
#        clave=self.cleaned_data.get("clave")
#        if Usuario.objects.get(id =  )