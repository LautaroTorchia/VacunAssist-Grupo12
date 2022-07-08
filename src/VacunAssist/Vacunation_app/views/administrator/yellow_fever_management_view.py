from Vacunation_app.forms.yellow_fever_turn_form import assigningYellowFeverTurn
from Vacunation_app.models import listaDeEsperaFiebreAmarilla, Turno
from Vacunation_app.turn_assignment import TurnAssignerYellowFever
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
import datetime


@permission_required("Vacunation_app.Administrador")
@login_required()
def yellow_fever_confirmation_view(request, id):
    petition = listaDeEsperaFiebreAmarilla.objects.get(id=id)
    form=assigningYellowFeverTurn(request.POST or None)
    if form.is_valid():
        fecha=datetime.datetime.combine(form.cleaned_data["fecha_del_turno"],form.cleaned_data["hora_del_turno"])
        try:
            if Turno.objects.get(fecha=fecha):
                messages.error(request,"Esa fecha y hora ya tiene un turno registrado, asigne otra fecha")
        except:
            TurnAssignerYellowFever(petition.paciente).assign_yellow_fever_turn(fecha,petition.vacunatorio)
            messages.success(request,f"turno asignado con exito en {fecha}")
            html_message = render_to_string('emails/exito_fiebre.html',{"fecha":fecha})
            send_mail("Registro de vacunador a VacunAssist",strip_tags(html_message),from_email=DEFAULT_FROM_EMAIL,recipient_list=[petition.paciente.user.email],
            fail_silently=False,html_message=html_message)
            petition.delete()
            return redirect(reverse("yellow_fever_list"))
    context = {"petition": petition, "form":form}
    return render(request, "administrator/yellow_fever_confirmation.html", context)

@permission_required("Vacunation_app.Administrador")
@login_required()
def reject_petition_view(request,id):
    petition = listaDeEsperaFiebreAmarilla.objects.get(id=id)
    messages.success(request,"Turno rechazado")
    html_message = render_to_string('emails/rechazo_fiebre.html',{})
    send_mail("Registro de vacunador a VacunAssist",strip_tags(html_message),from_email=DEFAULT_FROM_EMAIL,recipient_list=[petition.paciente.user.email],
    fail_silently=False,html_message=html_message)
    petition.delete()
    return redirect(reverse("yellow_fever_list"))