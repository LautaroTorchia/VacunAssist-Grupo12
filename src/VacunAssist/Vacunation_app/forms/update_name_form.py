from django import forms
from ..models import Vacunatorio


class NameUpdateForm(forms.Form):
    nombre_actual = forms.ModelChoiceField(required=False,
                                           widget=forms.Select,
                                           queryset=Vacunatorio.objects.all())
    nombre_nuevo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'oninvalid': "setCustomValidity('Completa este campo')"}))
