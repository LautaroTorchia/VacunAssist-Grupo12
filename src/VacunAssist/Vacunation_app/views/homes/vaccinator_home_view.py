from django.shortcuts import redirect, render
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
        self.extra_context={"editar_perfil_url":reverse("update_vaccinator",args=str(request.user.id))}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "logout" in request.POST:
            logout(request)
            return redirect("accounts/login/")
        return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
    
def zona_view(request):
    return render(request,"zona.html",{})

def notification_view(request):
    return render(request,"notifications.html",{})

def contact_view(request):
    return render(request,"contact.html",{})