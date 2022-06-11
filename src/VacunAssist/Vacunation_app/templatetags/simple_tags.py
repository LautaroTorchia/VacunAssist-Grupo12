from django import template

register = template.Library()

@register.simple_tag
def user_has_perm(user, permstring):
    """Checkea si un usuario user tiene los permisos de permstring
    usage: user_has_perm user permstring
    Así en el template

    Args:
        user: Un usuario del moselo Usuario
        permstring (str): se ve algo como "Vacunation_app.Administrador"

    Returns:
        boolean: Si tiene permisos
    """
    return user.has_perm(permstring)