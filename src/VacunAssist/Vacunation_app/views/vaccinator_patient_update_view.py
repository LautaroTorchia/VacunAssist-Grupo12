from django.shortcuts import render
from django.views.generic.edit import UpdateView
from Vacunation_app.models import Usuario
from Vacunation_app.forms.updating_user_form import UpdatingUserForm


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
            "success": request.session["success"]
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.success_url= self.request.path_info
        form= self.get_form()
        user= self.get_object()
        request.session["success"]=form.is_valid()
        if (form.cleaned_data["password"]=="" or user.check_password(form.cleaned_data["password"])) and user.zona==form.cleaned_data["zona"]:
            request.session["success"]=False
        return super().post(request, *args, **kwargs)