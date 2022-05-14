from .models import Usuario

def check_dni(dni):
    try:
        Usuario.objects.get(dni=dni)
    except:
        return len(dni)<15 and len(dni)>0
    return False


