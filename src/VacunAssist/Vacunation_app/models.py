from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import Permission
from django.forms import ValidationError
from django.db import models


def validate_alpha(nombre):
    if all(x.isalpha() or x.isspace()
           for x in nombre) and not nombre.isspace():
        raise ValidationError(f"El nombre solo puede tener letras y espacios")


def validate_decimal(dni):
    if not dni.isdecimal():
        raise ValidationError(f"El dni debe ser numerico")


class CustomUserManager(
        BaseUserManager
):  #Cambiar para que se vea más como elde la página o create superuser
    def create_user(self, dni, password, nombre_completo, fecha_nac, email,
                    clave, zona, **extra_fields):
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
        self.model = Usuario
        user = self.model()
        user.dni = dni
        user.email = email
        user.nombre_completo = nombre_completo
        user.fecha_nac = fecha_nac
        user.clave = clave
        user.set_password(password)
        user.zona = zona
        user.is_staff = extra_fields["is_staff"]
        user.is_superuser = extra_fields["is_superuser"]
        user.is_active = True
        user.save()

        return user

    def create_patient(self, dni, password, nombre_completo, fecha_nac,
                          email, clave,zona,covid,gripe,fiebre_amarilla,es_de_riesgo):
        extra_fields = {}
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        user = self.create_user(dni, password, nombre_completo, fecha_nac,
                                email, clave, zona, **extra_fields)

        user.user_permissions.set([Permission.objects.get(codename="Paciente")])
        patient_instance = Paciente.objects.create(user=user,dosis_covid=covid,
        fecha_gripe=gripe,tuvo_fiebre_amarilla=fiebre_amarilla,es_de_riesgo=es_de_riesgo)
        patient_instance.save()
        return patient_instance

    def create_vaccinator(self, dni, password, nombre_completo, fecha_nac,
                          email, clave, zona):
        extra_fields = {}
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        user = self.create_user(dni, password, nombre_completo, fecha_nac,
                                email, clave, zona, **extra_fields)
        user.user_permissions.set(
            [Permission.objects.get(codename="Vacunador")])
        vaccinator_instance = Vacunador.objects.create(user=user)
        vaccinator_instance.save()
        return user

    def create_administrator(self, dni, password, nombre_completo, fecha_nac,
                             email, clave):
        extra_fields = {}
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        zona = None
        user = self.create_user(dni, password, nombre_completo, fecha_nac,
                                email, clave, zona, **extra_fields)
        user.user_permissions.set(
            [Permission.objects.get(codename="Administrador")])
        administrator_instance = Administrador.objects.create(user=user)
        administrator_instance.save()
        return user

    def create_superuser(self, dni, password, nombre_completo, fecha_nac,
                         email, clave, **extra_fields):
        zona = None
        extra_fields = {}
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        return self.create_user(dni, password, nombre_completo, fecha_nac,
                                email, clave, zona, **extra_fields)


class Zona(models.Model):
    class Zonas(models.TextChoices):
        OMNIBUS = "Sede Omnibus"
        CEMENTERIO = "Sede Cementerio"
        MUNICIPALIDAD = "Sede Municipalidad"

    nombre = models.CharField(max_length=100,
                              choices=Zonas.choices,
                              unique=True)

    def __str__(self):
        return f"{self.nombre}"


class Usuario(AbstractUser):
    first_name = None
    last_name = None
    username = None
    REQUIRED_FIELDS = ["nombre_completo", "fecha_nac", "email", "clave"]
    objects = CustomUserManager()
    nombre_completo = models.CharField(max_length=50)  
    password = models.CharField(
        ('Contraseña'),
        max_length=128,
        validators=[
            MinLengthValidator(
                6, "Ingrese una contraseña de más de 6 caracteres")
        ])
    dni = models.CharField(max_length=15,
                           validators=[validate_decimal],
                           unique=True)
    fecha_nac = models.DateTimeField()
    email = models.EmailField(unique=True)
    clave = models.CharField(max_length=4)
    zona = models.ForeignKey(Zona, on_delete=models.RESTRICT, null=True)
    profile_pic=models.ImageField(default="profile_pic.png",blank=True,null=True)
    USERNAME_FIELD = 'dni'
    EMAIL_FIELD = 'email'
    is_active = models.BooleanField(
        "activo",
        default=True,
    )

    def get_absolute_url(self):
        return f"{self.id}"

    def get_full_name(self):
        return self.nombre_completo

    def __str__(self):
        return "Nombre: " + self.get_full_name() + " DNI: " + self.dni


class Paciente(models.Model):
    class Cantidad_dosis(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tuvo_fiebre_amarilla = models.BooleanField()
    dosis_covid = models.IntegerField(choices=Cantidad_dosis.choices)
    fecha_gripe = models.DateField()
    es_de_riesgo=models.BooleanField()

    class Meta:
        permissions = [
            ("Paciente",
             "Correspondiente al rol de Paciente en la documentación"),
        ]


    def __str__(self):
        return f"{self.user}"

class Administrador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("Administrador",
             "Correspondiente al rol de administrador en la documentación"),
        ]

    def __str__(self):
        return f"{self.user}"


class Vacuna(models.Model):
    class Vacunas(models.TextChoices):
        Gripe = "Gripe"
        COVID_PFIZER = "COVID_PFIZER"
        COVID_Astrazeneca = "COVID-Astrazeneca"
        Fiebre_amarilla = "Fiebre amarilla"

    nombre = models.CharField(max_length=100,
                              choices=Vacunas.choices,
                              unique=True)

    def __str__(self):
        return f"{self.nombre}"


class Vacunatorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    zona=models.ForeignKey(Zona,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

class Vacunador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("Vacunador",
             "Correspondiente al rol de Vacunador en la documentación"),
        ]

    def __str__(self):
        return f"{self.user}"

class VacunaEnVacunatorio(models.Model):
    vacunatorio = models.ForeignKey(Vacunatorio, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    stock = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.vacunatorio}-{self.vacuna}"


class Turno(models.Model):
    fecha=models.DateTimeField()
    vacunatorio=models.ForeignKey(Vacunatorio,on_delete=models.CASCADE)
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE)
    vacuna=models.ForeignKey(Vacuna,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.paciente.user.nombre_completo}- {self.fecha.date()} a las {self.fecha.time()} "

class listaDeEsperaCovid(models.Model):
    vacunatorio=models.ForeignKey(Vacunatorio,on_delete=models.CASCADE)
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE)
    vacuna=models.ForeignKey(Vacuna,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.paciente} - {self.vacuna}"

class listaDeEsperaFiebreAmarilla(models.Model):
    vacunatorio=models.ForeignKey(Vacunatorio,on_delete=models.CASCADE)
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE)
    vacuna=models.ForeignKey(Vacuna,on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return f"{self.id}"

    def __str__(self) -> str:
        return f"{self.paciente} - {self.vacunatorio}"