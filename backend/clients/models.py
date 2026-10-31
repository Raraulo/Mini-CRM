from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from .validators import validate_client_name


# Modelo persistido en SQLite: datos, estados y fechas del contacto.
class Client(models.Model):
    class Status(models.TextChoices):
        PROSPECT = 'prospect', 'Prospecto'
        CUSTOMER = 'customer', 'Cliente'
        INACTIVE = 'inactive', 'Inactivo'

    name = models.CharField('nombre', max_length=150, validators=[validate_client_name])
    company = models.CharField('empresa', max_length=150, blank=True)
    email = models.EmailField('correo electrónico')
    phone = models.CharField(
        'teléfono', max_length=30, blank=True,
        validators=[RegexValidator(
            regex=r'^\+?[0-9][0-9 ()-]{5,28}[0-9]$',
            message='Ingresa un teléfono de 7 a 30 caracteres con números, espacios, paréntesis o guiones. Puede comenzar con +.',
        )],
    )
    status = models.CharField(
        'estado', max_length=10, choices=Status.choices, default=Status.PROSPECT,
    )
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('última actualización', auto_now=True)

    class Meta:
        ordering = ['-created_at', '-pk']
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    # Normalización común antes de guardar desde formularios o código.
    def clean(self):
        super().clean()
        for field in ('name', 'company', 'email', 'phone'):
            value = getattr(self, field)
            if isinstance(value, str):
                setattr(self, field, value.strip())
        if not self.name:
            raise ValidationError({'name': 'El nombre es obligatorio.'})

    # Ejecuta las validaciones del modelo antes de escribir en la base.
    def save(self, *args, **kwargs):
        # Valida también los guardados desde código, además de los formularios.
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
