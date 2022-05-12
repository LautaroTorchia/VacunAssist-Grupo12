from django.shortcuts import render, get_object_or_404
from ..models import Vacunador


def vaccinator_delete_view(request, id):
    obj = get_object_or_404(Vacunador, id=id)
    if request.method == "POST":
        obj.delete()
    context = {"object": obj}
    return render(request, "products/products_delete.html", context)