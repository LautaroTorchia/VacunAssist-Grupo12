from django.urls import reverse_lazy
from django.views.generic import FormView
from typing import *
from django.http import HttpRequest,HttpResponse
from Vacunation_app.models import Usuario, Vacunacion, Vacunatorio, NonRegisteredVacunacion, Paciente
from Vacunation_app.forms.no_turn_form import NoTurnForm
from django.utils import timezone
from django.contrib import messages
from Vacunation_app.custom_functions import check_dni, vaccunassist_send_mail
from Vacunation_app.turn_assignment import update_stock, vaccinate


class NoTurnView(FormView):
    form_class=NoTurnForm
    template_name: str= "vaccinator/no_turn.html"
    success_url: Optional[str]=reverse_lazy("vaccinator_home")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunatorio=Vacunatorio.objects.get(zona=request.user.zona)
        form=self.get_form()
        if form.is_valid():
            dni=form.cleaned_data.get("dni")
            email=form.cleaned_data.get("email")
            vacuna=form.cleaned_data.get("vacuna")
            success,data=check_dni(dni)
            if not success and data["mensaje de error"] == "DNI ya registrado":
                try:
                    patient=Paciente.objects.get(user=Usuario.objects.get(dni=dni))
                    vacunacion=Vacunacion.objects.create(vacuna=vacuna
                    ,vacunatorio=vacunatorio,paciente=patient,fecha=timezone.now())
                    messages.success(request,f"Vacunación sin turno de {patient} registrada")
                    vaccinate(patient,vacuna)
                    update_stock(vacunatorio=vacunatorio,vacuna=vacuna)
                    vaccunassist_send_mail("emails/noturn_registered_vacunated_email.html",{"vacunacion":vacunacion,"paciente":patient,"login_url":request.build_absolute_uri('/accounts/login')},"Vacunación sin turno",email)
                except:
                    messages.error(request,"Sos parte del personal, no podes vacunarte")
            else:
                if success:
                    vacunacion=NonRegisteredVacunacion.objects.create(
                        vacuna=vacuna,vacunatorio=vacunatorio,dni=dni,nombre_completo=data["nombre"],fecha=timezone.now())
                    update_stock(vacunatorio=vacunatorio,vacuna=vacuna)
                    messages.success(request,f"Vacunación sin turno de {vacunacion.nombre_completo} registrada")
                    vaccunassist_send_mail("emails/nonregistered_vacunated_email.html",{"vacunacion":vacunacion,"register_url":request.build_absolute_uri('/accounts/registration')},"Vacunación sin turno",email)
                else:
                    messages.error(request,"El dni no es válido")
                    self.success_url: Optional[str]=reverse_lazy("vaccinator_no_turn")
        return super().post(request, *args, **kwargs)



