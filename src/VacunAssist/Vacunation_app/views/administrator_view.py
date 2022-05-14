import random
from django.shortcuts import redirect, render
from Vacunation_app.forms.stock_form import StockForm
from ..forms.creating_user_form import CreatingUserForm
from ..models import VacunaEnVacunatorio, Vacunador, Vacunatorio
import string
from django.core.mail import send_mail
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from ..custom_functions import check_dni


def administrator_home_view(request):
    return render(request, "administrator_view.html", {})


def creating_vaccinator_view(request):

    letters = string.ascii_lowercase
    user_creation_form = CreatingUserForm(request.POST or None)
    success=False
    dni_validated=False
    
    if "dni-validation" in request.POST:
        dni_validated=check_dni(request.POST["dni"])
    else:
        if user_creation_form.is_valid():
            user_instance = user_creation_form.save()
            password=''.join(random.choice(letters) for i in range(10))
            user_instance.set_password(password)
            user_instance.clave= ''.join(random.choice(letters) for i in range(4))
            user_instance.dni=user_creation_form.cleaned_data.get("dni")
            user_instance.save()
            vaccinator_instance=Vacunador.objects.create(user=user_instance)
            vaccinator_instance.save()
            user_creation_form = CreatingUserForm()
            success=True

            send_mail("Registro de vacunador a VacunAssist",
            f"""Hola, {user_instance.nombre_completo}
            Se ha registrado una cuenta en VacunAssist a su nombre aqui estan sus credenciales: 
            Contraseña: {password}
            clave:   {user_instance.clave}""",
                    DEFAULT_FROM_EMAIL,
                    [user_instance.email],
                    fail_silently=False)   
    context={ 
        "form": user_creation_form,
        "success": success,
        "dni_validated":dni_validated
        }

    return render(request, "vaccinator_creation.html",context)


def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)


def stock_view(request):

    vaccine_info=VacunaEnVacunatorio.objects.all()
    vaccination_center_info=Vacunatorio.objects.all()
    stock_form=StockForm(request.POST or None)
    
    #if stock_form.is_valid():
        #VacunaEnVacunatorio.objects.get(id=)
        

    context = {
        "vaccine_info": vaccine_info,
        "vaccination_center_info":vaccination_center_info,
        "stock_form":stock_form
    }
    return render(request, "stock_view.html", context)