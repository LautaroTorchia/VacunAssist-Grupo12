from django import forms
from Vacunation_app.models import Vacuna, Zona
from Vacunation_app.forms.p import PForm
from django.utils import timezone


Choices =(
    ("DNI", "DNI"),
    ("Vacuna", "Vacuna"),
    ("Zona", "Zona")
)

ChoicesOrder =(
    ("Ascendente", "Ascendente"),
    ("Descendente", "Descendente"),
)

class FiltersSelectorForm(PForm,forms.Form):

    error_messages = {
        "incorrect_dates": (
            "Las fechas estan cruzadas, introduzca fechas validas"
        ),
    }

    fecha_ini=forms.DateField(widget=forms.DateInput(attrs={'type': 'date',"min":"2010-01-01","max":timezone.now().date()}))
    fecha_fin=forms.DateField(widget=forms.DateInput(attrs={'type': 'date',"min":"2010-01-01","max":timezone.now().date()}))
    filter=forms.ChoiceField(choices=Choices,label="Filtro")
    order=forms.ChoiceField(choices=ChoicesOrder,label="Orden")
    dni_to_filter=forms.CharField(widget=forms.TextInput(),required=False,label="DNI a filtrar")
    vaccine_to_filter=forms.ModelChoiceField(widget=forms.Select,queryset=Vacuna.objects.all(),required=False,label="Vacuna a filtrar")
    zona_to_filter=forms.ModelChoiceField(widget=forms.Select,queryset=Zona.objects.all(),required=False,label="Zona a filtrar")


    def clean_fecha_fin(self):
        fecha_fin=self.cleaned_data["fecha_fin"]
        fecha_ini=self.cleaned_data["fecha_ini"]
        if fecha_ini>fecha_fin:
            raise forms.ValidationError(
                self.error_messages["incorrect_dates"],
                code="incorrect_dates",
            )
        return fecha_fin