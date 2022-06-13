from django.views.generic import RedirectView
from django.urls import reverse

class HomeRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        user=request.user

        if user.has_perm("Vacunation_app.Administrador"):    
            request.session["editar_perfil_url"]=reverse("admin_contact")
            self.pattern_name="admin_home"
            return super().get(request, *args, **kwargs)

        if user.has_perm("Vacunation_app.Vacunador"):
            request.session["editar_perfil_url"]=reverse("update_vaccinator",args=[str(user.id)])
            self.pattern_name="vaccinator_home"
            return super().get(request, *args, **kwargs)

        if user.has_perm("Vacunation_app.Paciente"):
            request.session["editar_perfil_url"]=reverse("update_user",args=[str(user.id)])
            self.pattern_name="user_home"
            return super().get(request, *args, **kwargs)

        self.pattern_name="login"
        return super().get(request, *args, **kwargs)