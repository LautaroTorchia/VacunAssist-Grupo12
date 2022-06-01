from django.shortcuts import redirect, render

from Vacunation_app.forms.creating_user_form import CreatingPatientForm


def registration_view(request):
    form=CreatingPatientForm(request.POST or None)
    return render(request,"registration/registration.html",{"form":form})