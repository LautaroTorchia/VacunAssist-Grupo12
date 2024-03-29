from datetime import datetime
from django.urls import reverse_lazy
from dotenv import load_dotenv
from Vacunation_app.models import Usuario
import requests
import random
import string
import os
from icalendar import Calendar, Event, vCalAddress, vText
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
from typing import Any
from django.http import HttpResponse,HttpRequest
from VacunAssist.settings import DEFAULT_FROM_EMAIL,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
from django.core.mail import get_connection,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils import timezone

def calculate_age(born):
    today = timezone.now().date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def vacunassist_send_mail(html_template,html_context: dict, subject, email, file_attachment=None)-> int:
        html_message = render_to_string(html_template, html_context)
        html_text=strip_tags(html_message)
        connection = get_connection(username=EMAIL_HOST_USER,password=EMAIL_HOST_PASSWORD)

        mail = EmailMultiAlternatives(
        subject, html_text, from_email=DEFAULT_FROM_EMAIL, to=[email], connection=connection
        )
        mail.attach_alternative(html_message, "text/html")

        if file_attachment:
            mail.attach("Certificado.pdf",content=file_attachment,mimetype="application/pdf")
        return mail.send()


def make_qr(data:str=reverse_lazy("login")):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image().convert('RGB')
    valija=Image.open(find_static_file("img/Logo_con_texto.png")).reduce((9,7))
    pos = ((img_qr.size[0] - valija.size[0]) // 2, (img_qr.size[1] - valija.size[1]) // 2)
    img_qr.paste(valija, pos)
    img_qr.save(find_static_file("qr/qr.png"), format="png")


def render_to_pdf(template_src, context_dict={}):
    html=render_to_string(template_src,context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
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

from dateutil.relativedelta import relativedelta
from icalendar import vCalAddress, vText

def create_turn_event(fecha,nombre,vacuna,vacunatorio):
    cal = Calendar()
    cal.add('prodid', '-//Vacunassist//vacunassist.com//')
    cal.add('version', '2.0')
    event = Event()
    event.add("summary",f"Turno de vacunacion de {vacuna} para {nombre}")
    event.add("description","Recuerde avisar de forma anticipada si no podrá asistir a su turno")
    event.add('dtstart', fecha)
    event.add('dtend', fecha+relativedelta(hours=1))
    event.add('dtstamp', fecha)
    organizer = vCalAddress('MAILTO:noreply@vacunassist.com')
    organizer.params['cn'] = vText('Vacunassist')
    event['organizer'] = organizer
    event['location'] = vText(f'{vacunatorio}')
    event['uid'] = f'{str(fecha)}/noreply@vacunassist.com'
    cal.add_component(event)
    return cal.to_ical()