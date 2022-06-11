from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario=get_user_model()


class HomeView(LoginRequiredMixin,TemplateView):
    template_name="homepage.html"
    permission_required = ("Vacunation_app.Vacunador", )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "logout" in request.POST:
            logout(request)
            return redirect("accounts/login/")
        return redirect("/")

