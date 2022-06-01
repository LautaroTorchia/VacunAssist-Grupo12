from django.views.generic import RedirectView


class HomeRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        user=request.user
        if user.has_perm("Vacunation_app.Administrador"):
            self.pattern_name="admin_home"
            return super().get(request, *args, **kwargs)

        if user.has_perm("Vacunation_app.Vacunador"):
            self.pattern_name="vaccinator_home"
            return super().get(request, *args, **kwargs)

        if user.has_perm("Vacunation_app.Paciente"):
            self.pattern_name="user_home"
            return super().get(request, *args, **kwargs)

        self.pattern_name="login"
        return super().get(request, *args, **kwargs)