from django.shortcuts import render, redirect
from ..models import Usuario
from django.contrib.auth.decorators import login_required, permission_required
from ..forms.updating_user_form import UpdatingUserForm

@permission_required("Vacunation_app.Administrador")
@login_required()
def vaccinator_delete_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    print(request.method)
    if request.method == "POST":
        print('adentro')
        vacunador.delete()
        return redirect('../../vaccinators_list/?')
    context = {"vacunador": vacunador}
    return render(request, "vaccinator_delete.html", context)

@permission_required("Vacunation_app.Administrador")
@login_required()
def edit_vaccinator_profile_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    vacunador_update_form = UpdatingUserForm(request.POST or None)
    success=False
    if vacunador_update_form.is_valid():
        vacunador.set_password(vacunador_update_form.cleaned_data["password"])
        vacunador.save()
        success=True
        vacunador_update_form = UpdatingUserForm()
    context = {"vacunador": vacunador, "form": vacunador_update_form,"success":success}
    return render(request, "edit_vaccinator_profile_view.html", context)