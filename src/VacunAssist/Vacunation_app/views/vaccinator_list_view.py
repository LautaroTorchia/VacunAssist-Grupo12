from django.shortcuts import render, redirect
from ..models import Usuario
from django.contrib.auth.decorators import login_required
from ..forms.updating_user_form import UpdatingUserForm


@login_required(login_url="/accounts/login")
def vaccinator_delete_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    print(request.method)
    if request.method == "POST":
        print('adentro')
        vacunador.delete()
        return redirect('../../vaccinators_list/?')
    context = {"vacunador": vacunador}
    return render(request, "vaccinator_delete.html", context)


@login_required(login_url="/accounts/login")
def edit_vaccinator_profile_view(request, id):
    vacunador = Usuario.objects.get(id=id)
    vacunador_update_form = UpdatingUserForm(request.POST or None)
    if vacunador_update_form.is_valid():
        vacunador.set_password(vacunador_update_form.cleaned_data["password"])
        vacunador.save()
    context = {"vacunador": vacunador, "form": vacunador_update_form}
    return render(request, "edit_vaccinator_profile_view.html", context)