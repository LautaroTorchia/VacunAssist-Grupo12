from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  render
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
        self.extra_context={'user': Usuario.objects.get(dni=request.session['dni'])}
        return TemplateView.get(self,request,args,kwargs)
    