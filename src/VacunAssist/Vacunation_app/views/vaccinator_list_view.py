from django.shortcuts import render, get_object_or_404, redirect
from ..models import Vacunador


def vaccinator_delete_view(request, id):
    obj = get_object_or_404(Vacunador, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../')
    context = {"object": obj}
    return render(request, "products/products_delete.html", context)