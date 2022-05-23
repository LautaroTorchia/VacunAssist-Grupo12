from django.contrib import admin
from .models import Administrador, Vacunador, Usuario,Vacuna,Vacunatorio,VacunaEnVacunatorio
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Vacunador)
admin.site.register(Administrador)
admin.site.register(Vacuna)
admin.site.register(Vacunatorio)
admin.site.register(VacunaEnVacunatorio)