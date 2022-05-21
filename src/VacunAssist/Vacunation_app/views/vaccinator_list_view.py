from django.shortcuts import render, get_object_or_404, redirect
from ..models import Vacunador, Usuario
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login")
def vaccinator_delete_view(request, id):
    obj = get_object_or_404(Vacunador, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../')
    context = {"object": obj}
    return render(request, "vaccinator_delete", context)


@login_required(login_url="/accounts/login")
def edit_vaccinator_profile_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    context = {"vacunador": vacunador}
    return render(request, "edit_vaccinator_profile_view.html", context)