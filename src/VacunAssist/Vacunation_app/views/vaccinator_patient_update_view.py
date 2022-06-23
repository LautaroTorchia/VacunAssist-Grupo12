from django.shortcuts import render
from django.views.generic.edit import UpdateView
from Vacunation_app.models import Paciente, Usuario
from Vacunation_app.forms.updating_user_form import UpdatingUserForm
from django.contrib import messages
from django.contrib.auth import login

class ProfileUpdate(UpdateView):
    form_class = UpdatingUserForm
    model = Usuario
    template_name= "edit_vaccinator_profile_view.html"
    permission_required = ("Vacunation_app.Vacunador","Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        self.initial={"zona": self.get_object().zona,"riesgo": Paciente.objects.get(user=self.get_object()).es_de_riesgo}
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
            password_success=password_check(request,user,form.cleaned_data)
            if any([zona_check(user,form.cleaned_data),profile_pic_check(user,form.cleaned_data),password_success,riesgo_check(user,form.cleaned_data)]):
                user.save()
                messages.success(request,"Cuenta editada con exito")
            if password_success:
                login(request, user)
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

def profile_pic_check(user,cleaned_data):
    if str(cleaned_data["profile_pic"])=="profile_pic.png":
        return False
    user.profile_pic=cleaned_data["profile_pic"]
    return True

def riesgo_check(user,cleaned_data):
    paciente=Paciente.objects.get(user=user)
    print("cleaned_data[riesgo]",cleaned_data["riesgo"])
    print("paciente.es_de_riesgo",paciente.es_de_riesgo)
    if cleaned_data["riesgo"]==paciente.es_de_riesgo:
        return False
    else:
        paciente.es_de_riesgo=cleaned_data["riesgo"]
        paciente.save()
        return True