from django.shortcuts import render

def administrator_home_view(request):
    return render(request, "administrator_view.html",{})


def creating_vaccinator_view(request):

    if request.method=="POST":
        print("Nombre del vacunador: ",request.POST["name"])
    return render(request, "vaccinator_creation.html",{})