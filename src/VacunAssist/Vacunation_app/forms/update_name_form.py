from django import forms
from ..models import Vacunatorio
from Vacunation_app.forms.p import PForm


class NameUpdateForm(PForm,forms.Form):
    nombre_actual = forms.ModelChoiceField(widget=forms.Select,
                                           queryset=Vacunatorio.objects.all())
    nombre_nuevo = forms.CharField(
        max_length=100,
        widget=forms.TextInput())
