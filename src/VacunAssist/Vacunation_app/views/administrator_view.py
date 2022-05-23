import random
from django.shortcuts import render
from Vacunation_app.forms.stock_form import StockForm
from ..forms.creating_user_form import CreatingUserForm, EnteringDniForm
from ..models import VacunaEnVacunatorio, Vacunador, Vacunatorio
import string
from django.core.mail import send_mail
from VacunAssist.settings import DEFAULT_FROM_EMAIL
from ..custom_functions import check_dni
from django.views.generic.edit import FormView
from ..forms.update_name_form import NameUpdateForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests



@login_required(login_url="/accounts/login")
def administrator_home_view(request):
    return render(request, "administrator_view.html", {})




@login_required(login_url="/accounts/login")
def validating_dni_for_vaccinator_view(request):
    dni_form = EnteringDniForm(request.POST or None)
    params={"dni":14276579}
    headers={
        "X-Api-Key": "jn7ROnxjDFz8CMprjTyd2jFVJG4gchEaHxrzhZg3",
        "Content-Type": "application/json",
    }
    if dni_form.is_valid():
        response = requests.post("https://hhvur3txna.execute-api.sa-east-1.amazonaws.com/dev/person/lookup", 
        data=params,headers=headers)
        print(response.status_code)
        print(response.text)
        request.session['dni_to_create']= dni_form.cleaned_data.get("dni")
        return redirect("/administrator/create_vaccinator/step2")
    
    return render(request,"dni_validation_view.html",{"form":dni_form})




@login_required(login_url="/accounts/login")
def creating_vaccinator_view(request):
    letters = string.ascii_lowercase
    numbers= string.digits
    user_creation_form = CreatingUserForm(request.POST or None)
    success=False

    if user_creation_form.is_valid():

        user_instance = user_creation_form.save(commit=False)
        user_instance.clave = ''.join(random.choice(numbers) for i in range(4))
        password = ''.join(random.choice(letters) for i in range(10))
        user_instance.set_password(password)
        user_instance.dni = request.session["dni_to_create"]
        user_instance.save()

        vaccinator_instance = Vacunador.objects.create(user=user_instance)
        vaccinator_instance.save()
        success=True
        user_creation_form = CreatingUserForm()

        send_mail("Registro de vacunador a VacunAssist",
                    f"""Hola, {user_instance.nombre_completo}
        Se ha registrado una cuenta en VacunAssist a su nombre aqui estan sus credenciales: 
        Contraseña: {password}
        clave:   {user_instance.clave}""",
                    DEFAULT_FROM_EMAIL, [user_instance.email],
                    fail_silently=False)

    context = {
        "form": user_creation_form,
        "success":success,
    }

    return render(request, "vaccinator_creation.html", context)




@login_required(login_url="/accounts/login")
def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)




@login_required(login_url="/accounts/login")
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





class NameUpdate(LoginRequiredMixin,FormView):
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
