from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import random
from Vacunation_app.models import Turno, Vacuna, Vacunador, Vacunatorio

def today(turnos,date):
    print(list(filter(lambda turno: turno.fecha==date,turnos)))
    return len(list(filter(lambda turno: turno.fecha==date,turnos)))

def assign_vaccine_turn(date,max_turns,vacunatorio,paciente,vacuna):
    vacuna=Vacuna.objects.get(nombre=vacuna)
    turnos=Turno.objects.all()
    while today(turnos,date)==max_turns:
        date+timedelta(days=1)
    Turno.objects.create(fecha=date,vacunatorio=vacunatorio,paciente=paciente,vacuna=vacuna)


def assign_turns(patient):
    vacunatorio=Vacunatorio.objects.get(zona=patient.user.zona)
    vacunadores=Vacunador.objects.all()
    cant_in_vacunatorio=len(list(filter(lambda vacunador: (vacunador.user.zona==patient.user.zona), vacunadores)))
    max_turns=8*4*cant_in_vacunatorio
    print(Vacuna.objects.get(nombre="Gripe"))
    if patient.es_de_riesgo:
        covid_date=date.today()+timedelta(days=7)
        gripe_date=date.today()+relativedelta(months=+3)
        assign_vaccine_turn(covid_date,max_turns,vacunatorio,patient,random.choice(["COVID-PFIZER","COVID-Astrazeneca"]))
    else:
        gripe_date=date.today()+relativedelta(months=+6)

    assign_vaccine_turn(gripe_date,max_turns,vacunatorio,patient,"Gripe")
    #assign_to_waitlist() #No esta pensado todavia esto!
