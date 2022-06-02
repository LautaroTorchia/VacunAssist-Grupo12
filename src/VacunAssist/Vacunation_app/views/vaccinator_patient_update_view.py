from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from Vacunation_app.models import Usuario
from Vacunation_app.forms.updating_user_form import UpdatingUserForm
from django.urls import reverse


class ProfileUpdate(UpdateView):
    form_class = UpdatingUserForm
    model = Usuario
    template_name= "edit_vaccinator_profile_view.html"
    permission_required = ("Vacunation_app.Vacunador","Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        self.initial={"zona": self.get_object().zona}
        try:
            success=request.session["success"]
        except:
            success=False
        context  = {
            "usuario": self.get_object(),
            "form": self.get_form(),
            "success": success
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        form= self.get_form()
        user= self.get_object()
        request.session["success"]=form.is_valid()

        request.session["success"]=any([zona_check(user,form.cleaned_data),password_check(user,form.cleaned_data)])
        if request.session["success"]:
            user.save()
        return super().post(request, *args, **kwargs)

def zona_check(user,cleaned_data):
    if user.zona!=cleaned_data["zona"]:
        user.zona=cleaned_data["zona"]
        return True
    return False

def password_check(user,cleaned_data):
    if not (cleaned_data["password"]=="" or user.check_password(cleaned_data["password"])):
        user.set_password(cleaned_data["password"])
        return True
    return False
