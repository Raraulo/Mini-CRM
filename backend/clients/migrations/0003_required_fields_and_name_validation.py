# Cambio histórico: validación del nombre y campos obligatorios en esta versión.

import clients.validators
from django.db import migrations, models
from django.core.validators import RegexValidator


class Migration(migrations.Migration):
    dependencies = [('clients', '0002_contactos_prueba')]
    operations = [
        migrations.AlterField(
            model_name='client', name='name',
            field=models.CharField(max_length=150, validators=[clients.validators.validate_client_name], verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='client', name='company',
            field=models.CharField(max_length=150, verbose_name='empresa'),
        ),
        migrations.AlterField(
            model_name='client', name='phone',
            field=models.CharField(max_length=30, verbose_name='teléfono', validators=[RegexValidator(
                regex=r'^\+?[0-9][0-9 ()-]{5,28}[0-9]$',
                message='Ingresa un teléfono de 7 a 30 caracteres con números, espacios, paréntesis o guiones. Puede comenzar con +.',
            )]),
        ),
    ]

