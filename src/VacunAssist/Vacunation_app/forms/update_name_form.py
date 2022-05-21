from django import forms
from ..models import Vacunatorio

class NameUpdateForm(forms.Form):
    nombre_actual=forms.ModelChoiceField(required=False, widget=forms.Select, queryset=Vacunatorio.objects.all())
    nombre_nuevo= forms.CharField(max_length=100)
    def print_clean_data(self):

        print(self.cleaned_data+"-"*500)

