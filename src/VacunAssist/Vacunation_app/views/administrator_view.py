import random
from django.shortcuts import render
from Vacunation_app.forms.stock_form import StockForm
from ..forms.creating_user_form import CreatingUserForm
from ..models import Vacuna, VacunaEnVacunatorio, Vacunador, Vacunatorio
import string
from django.core.mail import send_mail
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from ..custom_functions import check_dni
from django.views.generic.edit import FormView
from ..forms.update_name_form import NameUpdateForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect

def administrator_home_view(request):
    return render(request, "administrator_view.html", {})


def creating_vaccinator_view(request):

    letters = string.ascii_lowercase
    user_creation_form = CreatingUserForm(request.POST or None)
    success = False
    dni_validated = False

    if "dni-validation" in request.POST:
        dni_validated = check_dni(request.POST["dni"])
    else:
        if user_creation_form.is_valid():

            user_instance = user_creation_form.save()
            password = ''.join(random.choice(letters) for i in range(10))
            user_instance.set_password(password)
            user_instance.clave = ''.join(
                random.choice(letters) for i in range(4))
            user_instance.dni = user_creation_form.cleaned_data.get("dni")
            user_instance.save()

            vaccinator_instance = Vacunador.objects.create(user=user_instance)
            vaccinator_instance.save()
            user_creation_form = CreatingUserForm()

            success = True

            send_mail("Registro de vacunador a VacunAssist",
                      f"""Hola, {user_instance.nombre_completo}
            Se ha registrado una cuenta en VacunAssist a su nombre aqui estan sus credenciales: 
            Contraseña: {password}
            clave:   {user_instance.clave}""",
                      DEFAULT_FROM_EMAIL, [user_instance.email],
                      fail_silently=False)

    context = {
        "form": user_creation_form,
        "success": success,
        "dni_validated": dni_validated
    }

    return render(request, "vaccinator_creation.html", context)


def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)


def stock_view(request):

    vaccine_info = VacunaEnVacunatorio.objects.all()
    vaccination_center_info = Vacunatorio.objects.all()
    stock_form = StockForm(request.POST or None)
    updated = False

    if stock_form.is_valid():

        vacuna = stock_form.cleaned_data.get("vacuna")
        vacunatorio = stock_form.cleaned_data.get("vacunatorio")

        vacunation_to_update = VacunaEnVacunatorio.objects.get(
            vacuna=vacuna, vacunatorio=vacunatorio)
        vacunation_to_update.stock += stock_form.cleaned_data.get("stock")
        vacunation_to_update.save()
        updated = True
        stock_form = StockForm()

    context = {
        "vaccine_info": vaccine_info,
        "vaccination_center_info": vaccination_center_info,
        "stock_form": stock_form,
        "updated": updated
    }
    return render(request, "stock_view.html", context)


class NameUpdate(FormView):
    form=NameUpdateForm
    template_name="vacunatorio_name_update.html"
    def post(self, request, *args, **kwargs):
        instance_form=self.get_form(form_class=self.form)
        instance_form.is_valid()
        vacunatorio=instance_form.cleaned_data["nombre_actual"]
        nombre_nuevo=instance_form.cleaned_data["nombre_nuevo"]
        try:
            Vacunatorio.objects.get(nombre=nombre_nuevo)
            messages.error(self.request,"Vacunatorio ya existe")
        except Vacunatorio.DoesNotExist:
            vacunatorio.nombre=nombre_nuevo
            vacunatorio.save()
            messages.success(self.request,"Vacunatorio cambiado")
        return redirect("/administrator/cambiarNombre/")

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{"form":self.form})
