from django.urls import reverse_lazy
from django.views.generic import FormView
from typing import *
from django.http import HttpRequest,HttpResponse
from Vacunation_app.models import Usuario, Vacunacion, Vacunatorio, NonRegisteredVacunacion, Paciente
from Vacunation_app.forms.no_turn_form import NoTurnForm
from django.utils import timezone
from django.contrib import messages
from Vacunation_app.custom_functions import check_dni, vacunassist_send_mail


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

            try: 
                user=Usuario.objects.get(dni=dni)
                if Paciente.objects.filter(user=user).exists():     
                    patient=Paciente.objects.get(user=user)
                    vacunacion=Vacunacion.crear(vacuna=vacuna
                    ,vacunatorio=vacunatorio,paciente=patient,fecha=timezone.now())
                    messages.success(request,f"Vacunación sin turno de {patient} registrada")
                    vacunassist_send_mail("emails/noturn_registered_vacunated_email.html",{"vacunacion":vacunacion,"paciente":patient,"register_url":request.build_absolute_uri('/accounts/login')},"Vacunación sin turno",email)
                    return super().post(request, *args, **kwargs)
                else:
                    messages.error(request,"Sos parte del personal, no podes vacunarte")
                    return super().post(request, *args, **kwargs)
            except:
                success,data=check_dni(dni)
                if success:
                    vacunacion=NonRegisteredVacunacion.crear(
                        vacuna=vacuna,vacunatorio=vacunatorio,dni=dni,nombre_completo=data["nombre"],fecha=timezone.now())
                    messages.success(request,f"Vacunación sin turno de {vacunacion.nombre_completo} registrada")
                    vacunassist_send_mail("emails/nonregistered_vacunated_email.html",{"vacunacion":vacunacion,"register_url":request.build_absolute_uri('/accounts/registration')},"Vacunación sin turno",email)
                    return super().post(request, *args, **kwargs)
                
                if not success:
                    messages.error(request,"El dni no es válido")
                    self.success_url: Optional[str]=reverse_lazy("vaccinator_no_turn")
                    return super().post(request, *args, **kwargs)





