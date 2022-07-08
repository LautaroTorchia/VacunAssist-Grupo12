from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from typing import Any

class CustomPasswordChangeView(PasswordChangeView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.success_url=self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        self.success_url=self.request.META.get('HTTP_REFERER')
        if form.is_valid():
            messages.success(request,"Contraseña actualizada correctamente")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)