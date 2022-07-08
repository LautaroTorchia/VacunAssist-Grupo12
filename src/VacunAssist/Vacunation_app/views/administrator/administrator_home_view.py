from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse


@permission_required("Vacunation_app.Administrador", raise_exception=True)
@login_required()
def administrator_home_view(request):
    if "logout" in request.POST:
        logout(request)
        return redirect(reverse("login"))
    return render(request, "administrator/administrator_view.html", {})