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
        self.success_url= ""+f"{self.get_object().id}"
        self.initial={"zona": self.get_object().zona}
        success=False
        if self.get_form().is_valid():
            success=True
        context  = {
            "vacunador": self.get_object(),
            "form": self.get_form(),
            "success": success
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.success_url= ""+f"{self.get_object().id}"
        return super().post(request, *args, **kwargs)