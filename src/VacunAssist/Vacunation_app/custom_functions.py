from django.urls import reverse_lazy
from dotenv import load_dotenv
from Vacunation_app.models import Usuario
import requests
import random
import string
import os
load_dotenv()
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static_file
from PIL import Image
import qrcode
import os

def make_qr(data:str=reverse_lazy("login")):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image().convert('RGB')
    valija=Image.open(find_static_file("img/Logo_con_texto.PNG")).reduce((9,7))
    pos = ((img_qr.size[0] - valija.size[0]) // 2, (img_qr.size[1] - valija.size[1]) // 2)
    img_qr.paste(valija, pos)
    img_qr.save(find_static_file("qr/qr.png"), format="png")


def render_to_pdf(template_src, context_dict={}):
    html=render_to_string(template_src,context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

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

