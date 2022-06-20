#!/usr/bin/env python3
import email
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VacunAssist.settings')
django.setup()


from datetime import datetime
from Vacunation_app.models import CustomUserManager
from Vacunation_app.custom_functions import check_dni
dni=input("Ingrese el dni: ")
dnivalido,datos_de_la_persona=check_dni(dni)
if dnivalido:
    nombre_completo=datos_de_la_persona["nombre"]
    fecha_nac=datos_de_la_persona["fecha_nacimiento"]
else:
    raise RuntimeError
email=input("Ingrese el mail: ")
password=input("Ingrese el password: ")
clave=input("Ingrese la clave: ")

manager= CustomUserManager()
manager.create_administrator(dni=dni,password=password,nombre_completo=nombre_completo,
    fecha_nac=fecha_nac,email=email,clave=clave)

#39484790
#32147464 