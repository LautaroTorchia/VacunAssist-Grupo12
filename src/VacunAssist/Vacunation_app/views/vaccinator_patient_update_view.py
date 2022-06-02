from django.shortcuts import render
from django.views.generic.edit import UpdateView
from Vacunation_app.models import Usuario
from Vacunation_app.forms.updating_user_form import UpdatingUserForm
from django.contrib import messages


class ProfileUpdate(UpdateView):
    form_class = UpdatingUserForm
    model = Usuario
    template_name= "edit_vaccinator_profile_view.html"
    permission_required = ("Vacunation_app.Vacunador","Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        self.initial={"zona": self.get_object().zona}
        context  = {
            "usuario": self.get_object(),
            "form": self.get_form(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        form= self.get_form()
        user= self.get_object()
        if form.is_valid():
            success=any([zona_check(user,form.cleaned_data),
            password_check(request,user,form.cleaned_data),profile_pic_check(request,user,form.cleaned_data)])
            if success:
                user.save()
                messages.success(request,"Cuenta editada con exito")
        return super().post(request, *args, **kwargs)

def zona_check(user,cleaned_data):
    if user.zona==cleaned_data["zona"]:
        return False
    user.zona=cleaned_data["zona"]
    return True

def password_check(request,user,cleaned_data):
    if cleaned_data["password"]=="":
        return False
    if user.check_password(cleaned_data["password"]):
        messages.error(request,"La contraseña no puede ser la misma")
        return False
    user.set_password(cleaned_data["password"])
    return True

def profile_pic_check(request,user,cleaned_data):
    if not cleaned_data["profile_pic"]:
        return False
    user.profile_pic=cleaned_data["profile_pic"]
    return True