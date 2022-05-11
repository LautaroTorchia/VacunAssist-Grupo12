from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .constants import vacunas_opciones,vacunatorio_opciones


class Usuario(models.Model):
    
    nombre_completo = models.CharField(max_length=50)
    dni = models.IntegerField(unique=True,validators=[MaxValueValidator(999999999999999),MinValueValidator(1)])
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

    
class Vacuna(models.Model):
    nombre= models.CharField(max_length=50,choices=vacunas_opciones,unique=True)

    def __str__(self):
        return f"{self.nombre}"

class Vacunatorio(models.Model):
    nombre= models.CharField(max_length=50,choices=vacunatorio_opciones)

    def __str__(self):
        return f"{self.nombre}"

class VacunaEnVacunatorio(models.Model):
    vacunatorio=models.ForeignKey(Vacunatorio,on_delete=models.CASCADE)
    vacuna=models.ForeignKey(Vacuna,on_delete=models.CASCADE)
    stock= models.IntegerField()

    def __str__(self):
        return f"{self.vacunatorio}-{self.vacuna}"



from django.contrib.auth.models import (BaseUserManager)

