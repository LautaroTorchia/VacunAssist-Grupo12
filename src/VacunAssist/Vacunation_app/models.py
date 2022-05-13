from django.contrib.auth.backends import ModelBackend
from django.db import models
from  django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .constants import vacunas_opciones,vacunatorio_opciones
from django.contrib.auth.models import (BaseUserManager)
from django.core.validators import DecimalValidator
from django.core.exceptions import ValidationError

class UsuarioBackend(ModelBackend):
     def authenticate(self, request,**kwargs):
        dni = kwargs['dni']
        password = kwargs['password']
        try:
            usuario = Usuario.objects.get(dni=dni)
            if usuario.check_password(password) is True:
                return usuario.user
        except usuario.DoesNotExist:
            pass
        
class CustomUserManager( BaseUserManager):#Cambiar para que se vea más como elde la página o create superuser
    def create_user(self,dni,password,nombre_completo,fecha_nac,email,clave,**other_fields):
        if not dni:
            raise ValueError("El dni es obligatorio")
        if not nombre_completo:
            raise ValueError("El nombre completo es obligatorio")
        if not fecha_nac:
            raise ValueError("La fecha de nacimiento es obligatoria")
        if not email:
            raise ValueError("El email es obligatorio")
        if not clave:
            raise ValueError("La clave es obligatoria")
        email = self.normalize_email(email)
        user = self.model(dni,other_fields)
        user.email = email
        user.dni=dni
        user.nombre_completo = nombre_completo
        user.fecha_nac = fecha_nac
        user.clave = clave
        user.set_password(password)
        user.save()

    def create_superuser(self,dni,password,**extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(dni,password, **extra_fields)


def validate_decimal(dni):
        if not dni.isdecimal():
            raise ValidationError (f"El dni debe ser numerico")

def validate_alpha(nombre):
        if all(x.isalpha() or x.isspace() for x in nombre) and not nombre.isspace():
            raise ValidationError (f"El nombre solo puede tener letras y espacios")

class Usuario (AbstractUser):
    first_name = None
    last_name = None
    username = None
    REQUIRED_FIELDS = ["nombre_completo","fecha_nac","email","clave"]
    objects = CustomUserManager()
    nombre_completo = models.CharField(max_length=50)# ,validators=[validate_alpha])
    dni = models.CharField(max_length=15,validators=[validate_decimal],unique=True)
    fecha_nac = models.DateField()
    email = models.EmailField(unique=True)
    clave = models.CharField(max_length=4)
    USERNAME_FIELD= 'dni'
    EMAIL_FIELD='email'
    is_active=True
    def get_full_name(self):
        return self.nombre_completo
    def __str__(self):
        return self.get_full_name()
    

#class Usuario(models.Model):
#    
#    nombre_completo = models.CharField(max_length=50)
#    dni = models.IntegerField(unique=True,validators=[MaxValueValidator(999999999999999),MinValueValidator(1)])
#    fecha_nac = models.DateField()
#    email = models.EmailField(unique=True)
#    contrasenia = models.CharField(max_length=50)
#    clave = models.CharField(max_length=4)
#    
#
#    def __str__(self):
#        return self.nombre_completo


class Paciente(models.Model):
    class Cantidad_dosis(models.IntegerChoices):
        ZERO = 1
        ONE = 2
        TWO = 3

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tuvo_fiebre_amarilla = models.BooleanField()
    dosis_covid = models.IntegerField(choices=Cantidad_dosis.choices)
    fecha_gripe = models.DateField()

    def __str__(self):
        return f"{self.user}"


class Vacunador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    
class Vacuna(models.Model):
    class Vacunas(models.TextChoices):
        GRIPE_COMUN = "Gripe"
        COVID_F= "COVID-PFIZER"
        COVID_Z= "COVID-Astrazeneca"
        FIEBRE_A= "Fiebre amarilla"

    nombre= models.CharField(max_length=100,choices=Vacunas.choices,unique=True)

    def __str__(self):
        return f"{self.nombre}"

class Vacunatorio(models.Model):
    class Vacunatorios(models.TextChoices):
        OMNIBUS = "Sede Omnibus"
        CEMENTERIO= "Sede Cementerio"
        MUNICIPALIDAD= "Sede Municipalidad"
    
    nombre= models.CharField(max_length=100,choices=Vacunatorios.choices,unique=True)

    def __str__(self):
        return f"{self.nombre}"

class VacunaEnVacunatorio(models.Model):
    vacunatorio=models.ForeignKey(Vacunatorio,on_delete=models.CASCADE)
    vacuna=models.ForeignKey(Vacuna,on_delete=models.CASCADE)
    stock= models.IntegerField()

    def __str__(self):
        return f"{self.vacunatorio}-{self.vacuna}"

