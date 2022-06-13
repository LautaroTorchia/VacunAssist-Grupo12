from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse

from Vacunation_app.models import Paciente, Turno
Usuario=get_user_model()


class HomeView(LoginRequiredMixin,TemplateView):
    template_name="homepage.html"
    permission_required = ("Vacunation_app.Paciente", )

    def get(self, request, *args, **kwargs):
        self.extra_context={"editar_perfil_url":reverse("update_user",args=str(request.user.id))}
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
    try:
        paciente=Paciente.objects.get(user=request.user)
        turns=Turno.objects.filter(paciente=paciente)
        return render(request,"notifications.html",{"turns":turns})
    except:

        return render(request,"notifications.html",{"is_staff":"No tenes turnos asignados, ya que eres parte del personal"})
    
    

def contact_view(request):
    return render(request,"contact.html",{})