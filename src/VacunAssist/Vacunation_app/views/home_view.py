from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import  render
from django.contrib.auth import get_user_model
Usuario=get_user_model()

class HomeView(TemplateView):
    template_name="homepage.html"
    def get(self, request, *args, **kwargs):
        self.extra_context={'user': Usuario.objects.get(dni=request.session['dni'])}
        return render(request, self.template_name)
    