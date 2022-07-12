import os
from typing import Any
from django.http import HttpRequest, HttpResponse
from VacunAssist.settings import BASE_DIR
from Vacunation_app.custom_functions import  render_to_pdf
from Vacunation_app.custom_classes import AbstractPatientListView
from Vacunation_app.models import Paciente,Vacunacion
from PIL import Image,ImageDraw,ImageFont



class PaseSanitarioView(AbstractPatientListView):
    template_name: str="patient/pase_sanitario.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.queryset=Vacunacion.objects.none() 
        paciente=Paciente.objects.get(user=request.user)
        if paciente.dosis_covid==2:
            self.queryset=Vacunacion.objects.filter(paciente=paciente)
            self.queryset=list(filter(lambda x:"COVID" in x.vacuna.nombre,self.queryset))
            if len(self.queryset)<2:
                self.extra_context={"dosis_viejas":True}
                

        return super().get(request, *args, **kwargs)

    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        paciente=Paciente.objects.get(user=request.user)
        self.create_pase_sanitario(paciente)
        pdf=render_to_pdf("pdfs/pase_sanitario_pdf.html",context_dict={"paciente":paciente})
        return HttpResponse(pdf, content_type='application/pdf')
    
    def create_pase_sanitario(self,paciente):
        new = Image.new("RGBA", (900,500),color = (240, 240, 240))

        argentina_cuida = Image.open(os.path.join(BASE_DIR,"Vacunation_app/static/img/argentina_cuida.png"))
        argentina_cuida = argentina_cuida.resize((200,500))
        new.paste(argentina_cuida,(0,0))


        qr_pase = Image.open(os.path.join(BASE_DIR,"Vacunation_app/static/img/qr_pase.png"))
        qr_pase = qr_pase.resize((200,200))
        new.paste(qr_pase,(250,170))

        t1=ImageDraw.Draw(new)
        font_path_bold=os.path.join(BASE_DIR,"Vacunation_app/static/fonts/roboto/Roboto-Bold.ttf")
        font_path_not_bold=os.path.join(BASE_DIR,"Vacunation_app/static/fonts/roboto/Roboto-Regular.ttf")

        titulos = ImageFont.truetype(font_path_bold, 28, encoding="unic")
        subtitulos = ImageFont.truetype(font_path_not_bold, 23)
        datos_1 = ImageFont.truetype(font_path_not_bold, 15)
        datos_2 = ImageFont.truetype(font_path_bold, 15)

        t1.text((220, 15), "Vacunacion COVID-19", font=titulos, fill =(0, 0, 0))
        t1.text((220, 50), "COVID-19 Vaccination", font=subtitulos, fill =(0, 0, 0))

        t1.text((510, 190), "Apellido y nombre / Surname and given name", font=datos_1, fill =(0, 0, 0))
        t1.text((510, 230), f"{paciente.user.nombre_completo}", font=datos_2, fill =(0, 0, 0))
        t1.text((510, 300), "Documento / ID no.", font=datos_1, fill =(0, 0, 0))
        t1.text((510, 340), f"{paciente.user.dni}", font=datos_2, fill =(0, 0, 0))

        

        t1.text((220, 430), "Ministerio de Salud", font=titulos, fill =(0, 0, 0))
        t1.text((220, 460), "Ministry of Health", font=subtitulos, fill =(0, 0, 0))
        new.save(os.path.join(BASE_DIR,"Vacunation_app/static/img/pase_sanitario.png"))


