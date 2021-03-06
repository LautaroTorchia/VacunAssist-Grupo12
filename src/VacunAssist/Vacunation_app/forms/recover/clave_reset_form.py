from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

from Vacunation_app.forms.p import PForm


Usuario = get_user_model()

class ClaveResetForm(PForm,PasswordResetForm):

    email = forms.EmailField(
        label=(""),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'placeholder':"Email"}),
    )

    def save(
        self,
        domain_override=None,
        subject_template_name="emails/clave_reset_subject.txt",
        email_template_name="emails/clave_reset_email.html",
        use_https=False,
        token_generator="default_token_generator",
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        user= Usuario.objects.get(email=email)
        context={                
                "email": email,
                "user": user,
                "protocol": "https",}
        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            email,
        )

