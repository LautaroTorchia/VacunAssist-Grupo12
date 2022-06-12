from django.core.exceptions import ValidationError

class MinimumLengthValidator:
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ("Tu contraseña debe contener al menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return (
            "Tu contraseña debe contener al menos %(min_length)d caracteres."
            % {'min_length': self.min_length}
        )