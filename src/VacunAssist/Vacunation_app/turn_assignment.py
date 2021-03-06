from Vacunation_app.models import Paciente, Turno, Vacuna, Vacunador, Vacunatorio, listaDeEsperaCovid, listaDeEsperaFiebreAmarilla
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import random

class TurnAssigner():
    
    @staticmethod
    def get_assigner(paciente,fecha=None):
        if fecha:
            return TurnAssignerRisk(paciente.user,fecha) if paciente.es_de_riego_o_tiene_mas_de_60() else TurnAssignerNonRisk(paciente.user,fecha)
        else:
            return TurnAssignerRisk(paciente.user) if paciente.es_de_riego_o_tiene_mas_de_60() else TurnAssignerNonRisk(paciente.user)
    
    def __init__(self,user,gripe_date) -> None:
        self.patient=Paciente.objects.get(user=user)
        self.vacunatorio=Vacunatorio.objects.get(zona=self.patient.user.zona)
        self.gripe_date=gripe_date
        self.cant_in_vacunatorio=len(list(filter(lambda vacunador: (vacunador.user.zona==self.patient.user.zona), Vacunador.objects.all())))
        self.turnos=Turno.objects.all()

    def assign_turns(self):
        self.assign_covid_turn()
        self.assign_gripe_turn()
    
    def assign_covid_turn(self):
        pass #abstract

    def re_assign_covid_turn(self):
        if self.needs_covid_vaccine():
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            return  self.create_turn(self.covid_date)

    def needs_gripe_vaccine(self):
        gripe=Vacuna.objects.get(nombre="Gripe")
        return (self.patient.fecha_gripe+relativedelta(years=1) < timezone.now().date() 
        and not Turno.objects.filter(paciente=self.patient,vacuna=gripe).exists())
    
    def needs_covid_vaccine(self):
        return (self.patient.dosis_covid < 2) and (self.patient.user.fecha_nac.date()+relativedelta(years=18) <= timezone.now().date())
    
    def today_turns_are_full(self,date):
        return len(list(filter(lambda turno: turno.fecha.date()==date.date(),self.turnos)))==8*4*self.cant_in_vacunatorio
    
    def check_turn_hour(self,date):
        today_last_turns=list(filter(lambda turno: turno.fecha.date()==date.date(),self.turnos))[-self.cant_in_vacunatorio:]
        if today_last_turns:
            last_turn_date=today_last_turns[-1].fecha
            last_turn_time=last_turn_date.time()
            final_turn_date = date.replace(hour=last_turn_time.hour, minute=last_turn_time.minute,second=0)
            if len(today_last_turns)<self.cant_in_vacunatorio: 
                return final_turn_date
                
            cumplen=True
            for elem in today_last_turns:
                if elem.fecha.minute!=last_turn_time.minute:
                    cumplen=False
            if cumplen:
                return final_turn_date + relativedelta(minutes=15)
            
            return final_turn_date

        return date.replace(hour=8, minute=0,second=0)

    def create_amarilla_wait_list_request(self):
        self.vacuna=Vacuna.objects.get(nombre="Fiebre amarilla")
        listaDeEsperaFiebreAmarilla.objects.create(vacunatorio=self.vacunatorio,vacuna=self.vacuna,paciente=self.patient)            
    
    def create_turn(self,date):
        if self.cant_in_vacunatorio!=0:
            while self.today_turns_are_full(date):
                date+=relativedelta(days=1)

            date=self.check_turn_hour(date)
            return Turno.objects.create(fecha=date,vacunatorio=self.vacunatorio,paciente=self.patient,vacuna=self.vacuna)
            
    
    def assign_gripe_turn(self):
        if self.needs_gripe_vaccine():
            self.vacuna=Vacuna.objects.get(nombre="Gripe")
            return self.create_turn(self.gripe_date)
    

    
    def re_assign_covid_turn(self):
        if self.needs_covid_vaccine():
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            self.covid_date=self.covid_date+relativedelta(days=21)
            return  self.create_turn(self.covid_date)
    


class TurnAssignerRisk(TurnAssigner):
    def __init__(self, patient,reference_date=timezone.now()) -> None:
        self.old_turn_date=reference_date
        self.covid_date=reference_date+relativedelta(days=7)
        gripe_date=reference_date+relativedelta(months=+3)
        super().__init__(patient,gripe_date)
    

    def assign_covid_turn(self):
        if self.needs_covid_vaccine():
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            return  self.create_turn(self.covid_date)
    
    def re_assign_gripe_turn(self):
        self.vacuna=Vacuna.objects.get(nombre="Gripe")
        self.gripe_date=self.old_turn_date+relativedelta(days=7)
        return self.create_turn(self.gripe_date)

    

class TurnAssignerNonRisk(TurnAssigner):
    
    def __init__(self, patient,reference_date=timezone.now()) -> None:
        self.old_turn_date=reference_date
        self.covid_date=reference_date+relativedelta(days=14)
        gripe_date=reference_date+relativedelta(months=+6)
        super().__init__(patient,gripe_date)
    
    def create_wait_list_request(self):
        listaDeEsperaCovid.objects.create(vacunatorio=self.vacunatorio,vacuna=self.vacuna,paciente=self.patient)

    def assign_covid_turn(self):
        if self.needs_covid_vaccine():
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            self.create_wait_list_request()

    def re_assign_gripe_turn(self):
        self.vacuna=Vacuna.objects.get(nombre="Gripe")
        self.gripe_date=self.old_turn_date+relativedelta(months=+1)
        return self.create_turn(self.gripe_date)
    


class TurnAssignerYellowFever():
    patient=None
    vacuna=None
    def __init__(self, patient) -> None:
        self.patient = patient
        self.vacuna=Vacuna.objects.get(nombre="Fiebre amarilla")
    
    def assign_yellow_fever_turn(self,date,vacunatorio):
        return Turno.objects.create(fecha=date,vacunatorio=vacunatorio,paciente=self.patient,vacuna=self.vacuna)








