from datetime import date
from django import forms
from ..models import Vacunatorio
from Vacunation_app.forms.p import PForm


Choices =(
    ("DNI", "DNI"),
    ("Edad", "Edad"),
    ("Vacuna", "Vacuna"),
    ("Zona", "Zona"),
    ("Marca-COVID", "Marca-COVID"),
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

    fecha_ini=forms.DateField(widget=forms.DateInput(attrs={'type': 'date',"min":"2010-01-01","max":date.today()}))
    fecha_fin=forms.DateField(widget=forms.DateInput(attrs={'type': 'date',"min":"2010-01-01","max":date.today()}))
    filter=forms.ChoiceField(choices=Choices)
    order=forms.ChoiceField(choices=ChoicesOrder)


    def clean_fecha_fin(self):
        fecha_fin=self.cleaned_data["fecha_fin"]
        fecha_ini=self.cleaned_data["fecha_ini"]
        if fecha_ini>fecha_fin:
            raise forms.ValidationError(
                self.error_messages["incorrect_dates"],
                code="incorrect_dates",
            )
        return fecha_fin