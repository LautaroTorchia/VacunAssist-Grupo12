from Vacunation_app.forms.updating_user_form import UpdatingUserForm
from Vacunation_app.models import Paciente, Usuario
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

class ProfileUpdate(UpdateView):
    form_class = UpdatingUserForm
    model = Usuario
    template_name= "edit_profile_view.html"
    permission_required = ("Vacunation_app.Vacunador","Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        if self.get_object().has_perm("Vacunation_app.Paciente"):
            self.initial={"zona": self.get_object().zona,"riesgo": Paciente.objects.get(user=self.get_object()).es_de_riesgo}
        elif self.get_object().has_perm("Vacunation_app.Vacunador"):
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
        if "Aceptar" in request.POST:
            if form.is_valid():
                if any([zona_check(user,form.cleaned_data),profile_pic_check(user,form.cleaned_data),riesgo_check(user,form.cleaned_data)]):
                    user.save()
                    messages.success(request,"Cuenta editada con exito")
            return super().post(request, *args, **kwargs)
        elif "update_password" in request.POST:
            return redirect(reverse("update_user_password",args=[user.id]))

def zona_check(user,cleaned_data):
    if user.zona==cleaned_data["zona"]:
        return False
    user.zona=cleaned_data["zona"]
    return True

def profile_pic_check(user,cleaned_data):
    if str(cleaned_data["profile_pic"])=="profile_pic.png":
        return False
    user.profile_pic=cleaned_data["profile_pic"]
    return True

def riesgo_check(user,cleaned_data):
    paciente=Paciente.objects.get(user=user)
    if cleaned_data["riesgo"]==paciente.es_de_riesgo:
        return False
    else:
        paciente.es_de_riesgo=cleaned_data["riesgo"]
        paciente.save()
        return True