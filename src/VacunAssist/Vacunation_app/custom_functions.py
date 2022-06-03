import os
import random
import string
from .models import Usuario
import requests
from dotenv import load_dotenv

load_dotenv()


def check_dni(dni):
    datos_de_la_persona = {
        "nombre": "",
        "fecha_nacimiento": "",
        "mensaje de error": "",
    }
    try:
        Usuario.objects.get(dni=dni)
        datos_de_la_persona['mensaje de error'] = "DNI ya registrado"
        return False, datos_de_la_persona
    except:
        headers = {
            'X-Api-Key': os.getenv("DNI_VALIDATION_API"),
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                'https://hhvur3txna.execute-api.sa-east-1.amazonaws.com/dev/person/lookup',
                headers=headers,
                json={"dni": dni})
            if response.status_code == 200:
                if 'nombre' in response.json().keys():
                    datos_de_la_persona['nombre'] = response.json(
                    )['nombre'].title() + ' ' + response.json(
                    )['apellido'].title()
                else:
                    datos_de_la_persona['nombre'] = response.json(
                    )['apellido'].title()
                datos_de_la_persona['fecha_nacimiento'] = response.json(
                )['fechaNacimiento']
                return True, datos_de_la_persona
            else:
                datos_de_la_persona[
                    'mensaje de error'] = "No se pudo validar el DNI, intente nuevamente"
                return False, datos_de_la_persona
        except requests.exceptions.ConnectionError as e:
            datos_de_la_persona[
                'mensaje de error'] = "Ocurrio un error en la conexion con el servidor de validacion"
            return False, datos_de_la_persona


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer


def generate_keycode():
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(4))

def generate_random_password():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
