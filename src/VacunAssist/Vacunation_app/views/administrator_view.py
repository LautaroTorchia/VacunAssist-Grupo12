from django.shortcuts import render
from ..forms.creating_user_form import CreatingUserForm
from ..models import Vacunador


def administrator_home_view(request):
    return render(request, "administrator_view.html", {})


def creating_vaccinator_view(request):

    user_creation_form = CreatingUserForm(request.POST or None)
    if user_creation_form.is_valid():
        print(user_creation_form.cleaned_data)

    return render(request, "vaccinator_creation.html",
                  {"form": user_creation_form})


def vaccinators_list_view(request):
    queryset = Vacunador.objects.all()
    context = {"object_list": queryset}
    return render(request, "vaccinators_list.html", context)