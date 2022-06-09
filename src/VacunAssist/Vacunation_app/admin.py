from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Vacunador)
admin.site.register(Administrador)
admin.site.register(Vacuna)
admin.site.register(Vacunatorio)
admin.site.register(VacunaEnVacunatorio)
admin.site.register(Zona)
admin.site.register(Turno)
admin.site.register(listaDeEsperaCovid)