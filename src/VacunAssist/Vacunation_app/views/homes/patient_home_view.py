from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
Usuario=get_user_model()


class HomeView(LoginRequiredMixin,TemplateView):
    template_name="homepage.html"

    def post(self, request, *args, **kwargs):
        if "logout" in request.POST:
            logout(request)
            return redirect("accounts/login/")
        return redirect("/")

    def get(self, request, *args, **kwargs):
        try:
            if request.user.has_perm("Vacunation_app.Administrador"):
                return redirect("/administrator")
            return TemplateView.get(self,request,args,kwargs)
        except:
            return redirect("accounts/login/")

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
    
def zona_view(request):
    return render(request,"zona.html",{})

def notification_view(request):
    return render(request,"notifications.html",{})

def contact_view(request):
    return render(request,"contact.html",{})