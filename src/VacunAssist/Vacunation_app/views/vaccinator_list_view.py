from django.shortcuts import render, redirect
from ..models import Usuario
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse


@permission_required("Vacunation_app.Administrador")
@login_required()
def vaccinator_delete_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    print(request.method)
    if request.method == "POST":
        vacunador.delete()
        return redirect(reverse("vaccinators_list"))
    context = {"vacunador": vacunador}
    return render(request, "vaccinator_delete.html", context)

