from pyexpat import model
from django.db import models


class Usuario(models.Model):
    
    nombre_completo = models.CharField(max_length=50)
    dni = models.IntegerField(max_length=15, unique=True)
    fecha_nac = models.DateField()
    email = models.EmailField(unique=True)
    contrasenia = models.CharField(max_length=50)
    clave = models.CharField(max_length=4)

    def __str__(self):
        return self.nombre_completo


class Paciente(models.Model):
    class Suit(models.IntegerChoices):
        ZERO = 1
        ONE = 2
        TWO = 3

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tuvo_fiebre_amarilla = models.BooleanField()
    dosis_covid = models.IntegerField(choices=Suit.choices)
    fecha_gripe = models.DateField()

    def __str__(self):
        return f"{self.user}"


class Vacunador(models.Model):

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

from django.contrib.auth.models import (BaseUserManager)

