from django.urls import reverse_lazy
from django.views.generic import FormView
from typing import *
from django.http import HttpRequest,HttpResponse
from Vacunation_app.models import Usuario, Vacunacion, Vacunatorio, NonRegisteredVacunacion, Paciente
from Vacunation_app.forms.no_turn_form import NoTurnForm
from django.utils import timezone
from django.contrib import messages
from Vacunation_app.custom_functions import check_dni
from Vacunation_app.turn_assignment import vaccinate

class NoTurnView(FormView):
    form_class=NoTurnForm
    template_name: str= "vaccinator/no_turn.html"
    success_url: Optional[str]=reverse_lazy("vaccinator_home")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vacunatorio=Vacunatorio.objects.get(zona=request.user.zona)
        form=self.get_form()
        if form.is_valid():
            dni=form.cleaned_data.get("dni")
            success,data=check_dni(dni)
            if not success and data["mensaje de error"] == "DNI ya registrado":
                try:
                    patient=Paciente.objects.get(user=Usuario.objects.get(dni=dni))
                    vacunacion=Vacunacion.objects.create(vacuna=form.cleaned_data.get("vacuna"),vacunatorio=vacunatorio,paciente=patient,fecha=timezone.now())
                    messages.success(request,f"Vacunación sin turno de {patient} registrada")
                except:
                    messages.error(request,"Sos parte del personal, no podes vacunarte")
                vaccinate(patient,form.cleaned_data.get("vacuna"))
            else:
                if success:
                    vacunacion=NonRegisteredVacunacion.objects.create(
                        vacuna=form.cleaned_data.get("vacuna"),vacunatorio=vacunatorio,dni=dni,nombre_completo=data["nombre"],fecha=timezone.now())
                    messages.success(request,f"Vacunación sin turno de {vacunacion.nombre_completo} registrada")
                else:
                    messages.error(request,"El dni no es válido")
                    self.success_url: Optional[str]=reverse_lazy("vaccinator_no_turn")
        return super().post(request, *args, **kwargs)