from Vacunation_app.custom_classes import AdministratorPermissionsMixin
from Vacunation_app.custom_functions import generate_keycode, generate_random_password, get_referer,check_dni, vacunassist_send_mail
from Vacunation_app.forms.creating_user_form import CreatingVaccinatorForm,EnteringDniForm
from Vacunation_app.models import CustomUserManager, Vacunador
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import FormView
from typing import Any,Optional

class ValidateVaccinatorDNI(AdministratorPermissionsMixin,FormView):
    form_class=EnteringDniForm
    template_name: str="administrator/dni_validation_view.html"
    success_url: Optional[str]=reverse_lazy("create_vaccinator_step2")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form=self.get_form()
        if form.is_valid():
            dni = form.cleaned_data.get("dni")
            success, data = check_dni(dni)
            if success:
                request.session['vaccinator_data']={"dni":dni,"fecha_nacimiento":data["fecha_nacimiento"],"nombre":data["nombre"]}
                return redirect(self.success_url)
            else:
                messages.error(request, data["mensaje de error"])
                return redirect(reverse_lazy("creating_vaccinator_view"))
        return super().post(request, *args, **kwargs)


class CreateVaccinatorDNI(AdministratorPermissionsMixin,FormView):
    template_name: str="administrator/vaccinator_creation.html"
    form_class=CreatingVaccinatorForm
    success_url: Optional[str]=reverse_lazy("creating_vaccinator_view")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not get_referer(request):
            return redirect(reverse("creating_vaccinator_view"))
        context_data=request.session["vaccinator_data"]
        self.extra_context = {
        "DNI": context_data["dni"],
        "nombre": context_data["nombre"]}
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form=self.get_form()
        if form.is_valid():
            password = generate_random_password()
            clave = generate_keycode()
            context_data=request.session["vaccinator_data"]
            nombre_completo=context_data.get("nombre")
            email=form.cleaned_data.get("email")
            CustomUserManager().create_vaccinator(context_data.get("dni"), password,nombre_completo,context_data.get("fecha_nacimiento"),
            email,clave,form.cleaned_data.get("zona"))
            vacunassist_send_mail("emails/register_vaccinator_email.html"
            ,{"password":password,"clave":clave,"nombre_completo":nombre_completo},"Registro de vacunador a VacunAssist",email)
            messages.success(request, "Cuenta creada Correctamente")
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
