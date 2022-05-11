import random
from django.shortcuts import render
from ..forms.creating_user_form import CreatingUserForm
from ..models import Vacunador
import string
from django.core.mail import send_mail
from django.conf import settings


def administrator_home_view(request):
    return render(request, "administrator_view.html", {})


def creating_vaccinator_view(request):

    letters = string.ascii_lowercase
    user_creation_form = CreatingUserForm(request.POST or None)
    success=False

    
    if user_creation_form.is_valid():

        user_instance = user_creation_form.save()
        user_instance.contrasenia= ''.join(random.choice(letters) for i in range(10)) 
        user_instance.clave= ''.join(random.choice(letters) for i in range(4))
        user_instance.save()
        vaccinator_instance=Vacunador.objects.create(user=user_instance)
        vaccinator_instance.save()
        user_creation_form = CreatingUserForm()
        success=True

        #send_mail("Registro de vacunador a VacunAssist",
        #f"""Se ha registrado una cuenta a su nombre aqui estan sus credenciales: 
                #Contraseña: {instance.contrasenia}
                #clave:   {instance.clave}""",
                #settings.DEFAULT_FROM_EMAIL,
                #["torchia.lautaro2@gmail.com"],
                #fail_silently=False)
        
    context={ 
        "form": user_creation_form,
        "success": success,
        }

    return render(request, "vaccinator_creation.html",context)


def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)