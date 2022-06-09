from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import random
from Vacunation_app.models import Turno, Vacuna, Vacunador, Vacunatorio, listaDeEsperaCovid

class TurnAssigner():

    def __init__(self,patient,gripe_date) -> None:
        self.vacunatorio=Vacunatorio.objects.get(zona=patient.user.zona)
        self.patient=patient
        self.gripe_date=gripe_date
        print("fecha de turno potencial de gripe:",self.gripe_date)
        self.cant_in_vacunatorio=len(list(filter(lambda vacunador: (vacunador.user.zona==patient.user.zona), Vacunador.objects.all())))
        self.turnos=Turno.objects.all()

    def assign_turns(self):
        self.assign_covid_turn()
        self.assing_gripe_turn()
    
    def assign_covid_turn(self):
        pass #abstract

    def needs_gripe_vaccine(self):
        print("fecha",self.patient.fecha_gripe)
        return self.patient.fecha_gripe+relativedelta(years=1) < date.today()
    
    def needs_covid_vaccine(self):
        print("dosis",self.patient.dosis_covid)
        return self.patient.dosis_covid < 2
    
    def today_turns_are_full(self,date):
        return len(list(filter(lambda turno: turno.fecha==date,self.turnos)))
    
    def create_turn(self,date):
        while self.today_turns_are_full(date):
            date+timedelta(days=1)
        Turno.objects.create(fecha=date,vacunatorio=self.vacunatorio,paciente=self.patient,vacuna=self.vacuna)
    
    def assing_gripe_turn(self):
        if self.needs_gripe_vaccine():
            self.vacuna=Vacuna.objects.get(nombre="Gripe")
            self.create_turn(self.gripe_date)
            
    


class TurnAssignerRisk(TurnAssigner):
    def __init__(self, patient) -> None:
        self.covid_date=date.today()+timedelta(days=7)
        gripe_date=date.today()+relativedelta(months=+3)
        super().__init__(patient,gripe_date)
    

    def assign_covid_turn(self):
        if self.needs_covid_vaccine():
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            self.create_turn(self.covid_date)


class TurnAssignerNonRisk(TurnAssigner):
    
    def __init__(self, patient) -> None:
        gripe_date=date.today()+relativedelta(months=+6)
        super().__init__(patient,gripe_date)
    
    def create_wait_list_request(self):
        listaDeEsperaCovid.objects.create(vacunatorio=self.vacunatorio,vacuna=self.vacuna,paciente=self.patient)

    def assign_covid_turn(self):
        if self.needs_covid_vaccine:
            self.vacuna=Vacuna.objects.get(nombre=random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
            self.create_wait_list_request()