# Validación compartida del nombre para formularios y guardados del modelo.

import unicodedata

from django.core.exceptions import ValidationError


def validate_client_name(value):
    """Acepta letras Unicode, acentos, espacios, apóstrofes y guiones."""
    value = value.strip()
    if not any(character.isalpha() for character in value) or any(
        not (unicodedata.category(character).startswith(('L', 'M'))
             or character in " '-’")
        for character in value
    ):
        raise ValidationError('El nombre solo puede contener letras, espacios, apóstrofes y guiones.')
