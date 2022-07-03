from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

Usuario=get_user_model()

class HomeView(LoginRequiredMixin,TemplateView):
    template_name="vaccinator/vaccinator_homepage.html"
    permission_required = ("Vacunation_app.Vacunador", )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "logout" in request.POST:
            logout(request)
            return redirect(reverse("login"))
        return redirect("/")

